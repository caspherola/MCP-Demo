from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.client import MultiServerMCPClient

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
model = ChatOllama(model="llama3.2:3b")

server_params = StdioServerParameters(
    command="python3.12",
    # Make sure to update to the full absolute path to your math_server.py file
    args=["./mcp_server.py"],
)

async def main(query: str):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # Create and run the agent
            agent = create_react_agent(model, tools)
            agent_response = await agent.ainvoke({"messages": query})
            return agent_response

# Run the async function
import asyncio
query1="what is the current weather in california"
response1 = asyncio.run(main(query1))
print(response1["messages"][3].content)
query2="any weather alert in texes"
response2 = asyncio.run(main(query2))
print(response2["messages"][3].content)