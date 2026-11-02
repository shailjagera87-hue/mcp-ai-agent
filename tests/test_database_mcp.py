import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def test_database_mcp():

    server_url = "http://127.0.0.1:8003/mcp"

    async with streamablehttp_client(server_url) as (
        read_stream,
        write_stream,
        _
    ):

        async with ClientSession(read_stream, write_stream) as session:

            # Initialize connection with MCP server
            await session.initialize()

            # Discover available tools
            tools = await session.list_tools()

            print("\nAvailable Database MCP Tools:")

            for tool in tools.tools:
                print(f"- {tool.name}")

            # Example: Call a database tool
            # Change "get_all_customers" if your tool has a different name.
            result = await session.call_tool(
                "get_all_customers",
                arguments={}
            )

            print("\nDatabase Tool Result:")
            print(result)


if __name__ == "__main__":
    asyncio.run(test_database_mcp())