# Local Agent
This is a local agent that can be used to run LangChain agents locally. It is built using FastAPI and Docker.

## Current Status
- Only initial setup is done.
- Agent is working.
- Agent have memory. 
- Only supports Ollama model for now. (Will add more models in future)

## Future Plans
- Add more tools in mcp server
- Add more error handling and logging to the agent
- Add streaming API
- Add chainlit ui
- Dynamic model support
- May add more features like voice support, etc.

## To Start The Local Agent
### Docker
`docker compose up`

### Directly
`uv venv`
`uv sync`
`cd fast_api_agent`
`uv run fastapi run api_endpoints.py`

## To Access The Local Agent
Swagger UI : `http://localhost:8000/docs`

## Pre-requisites
- Docker installed on your machine
- Ollama