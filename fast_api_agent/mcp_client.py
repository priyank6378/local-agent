from langchain_mcp_adapters.client import MultiServerMCPClient

client = MultiServerMCPClient(
    {
        "local" : {
            "transport": "streamable_http",
            "url": "http://localhost:8001/mcp"
        }
    }
)

