import asyncio

from app.mcp_client.manager import MCPClientManager


async def main():

    async with MCPClientManager() as manager:

        print("MCP connections initialized")

        for server_name, session in manager.sessions.items():
            tools = await manager.get_tools(server_name) if hasattr(
                manager, "get_tools"
            ) else await session.list_tools()

            print(f"\n{server_name.upper()}")

            for tool in tools.tools:
                print(f"Tool: {tool.name}")
                print(f"Description: {tool.description}")


if __name__ == "__main__":
    asyncio.run(main())