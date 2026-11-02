import asyncio

from app.mcp_client.manager import MCPClientManager


async def main():

    manager = MCPClientManager()

    try:

        tools = await manager.connect_to_server(
            "weather",
            "http://127.0.0.1:8001/mcp"
        )

        print("Connected successfully")

        for tool in tools:
            print(tool.name)

    finally:
        await manager.disconnect_all()


if __name__ == "__main__":
    asyncio.run(main())