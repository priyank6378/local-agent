from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import ToolMessage, HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langchain_ollama import ChatOllama
# from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row
import psycopg

import logging
import asyncio
import sys 


logging.basicConfig(level=logging.WARNING)
# logging.getLogger(".").setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.info("Logging initialized")


from settings import AgentSettings



class MyAgent():
    def __init__(self):
        # lightweight synchronous init; heavy async work happens in `create`
        self.settings = AgentSettings()
        self._db_url = self.settings.db_url

        self.checkpointer = None
        self.tools = None
        self.model = None
        self.agent = None

    @classmethod
    async def create(cls):
        logger.info("Creating Agent...")

        from mcp_client import client

        self = cls()
        # fetch async resources
        try:
            self.tools = await client.get_tools()
        except Exception as e:
            logger.error(e)
            self.tools = []
        # create checkpointer
        self.checkpointer = await self._create_checkpointer(self._db_url)

        self.model = ChatOllama(
            model=self.settings.model,
            system_prompt="you are helpful chatbot. Use the tools when you think it is needed."
        )

        self.agent = create_agent(
            model=self.model,
            tools=self.tools,
            checkpointer=self.checkpointer
        )
        return self

    async def _create_checkpointer(self, db_url: str|None = None):
        if db_url:
            logger.info(f"Tyring {db_url}")
            conn = await psycopg.AsyncConnection.connect(
                conninfo=db_url,
                autocommit=True,
                row_factory=dict_row,
            )
            checkpointer = AsyncPostgresSaver(conn)
            try:
                await checkpointer.setup()
                logger.info("Created checkpointer for database")
                return checkpointer
            except Exception as e:
                logger.error(e)
                exit(0)
        else:
            return InMemorySaver()

    def _call_tool(self, response):
        pass

    async def invoke(self, message: str, config: dict | None = None):
        response = await self.agent.ainvoke({
                "messages" : [HumanMessage(message)],
            }, 
            config
        )

        return response["messages"][-1].content

    async def agentic_loop(self):
        config = {"configurable": {"thread_id": 1}}
        user = input("> ")
        while user != r"\q":
            response = await self.invoke(user, config)
            print(response)
            user = input("> ")
        


if __name__=="__main__" :
    
    async def main():
        agent = await MyAgent.create()
        await agent.agentic_loop()

    asyncio.run(main())

