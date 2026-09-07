from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel, Field

from agent import MyAgent


class AgentQuestion(BaseModel):
    question: str
    context_id: str | None = None

agent = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global agent
    agent = await MyAgent.create()
    yield

app = FastAPI(title="my app", lifespan=lifespan)


@app.get("/health")
def health():
    return "OK"

@app.post("/predict")
async def generate_output(question: AgentQuestion):
    config = {"configurable": {"thread_id": question.context_id}}
    response = await agent.invoke(question.question, config)

    return response