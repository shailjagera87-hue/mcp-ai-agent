
import asyncio

from app.mcp_client.manager import MCPClientManager


async def main():

    manager = MCPClientManager()

    try:

        # Connect to all servers
        results = await manager.connect_all()

        print("\nSERVER CONNECTION STATUS")

        for name, result in results.items():

            print(name, result["connected"])

            if not result["connected"]:
                print(result.get("error"))

        # Discover all tools
        all_tools = await manager.discover_all_tools()

        print("\nDISCOVERED TOOLS")

        for server_name, tools in all_tools.items():

            for tool in tools:
                print(
                    f"{server_name}_{tool.name}"
                )

        # Test weather
        if "weather" in manager.sessions:

            result = await manager.call_tool(
                "weather",
                "get_weather",
                {"city": "Delhi"}
            )

            print("\nWEATHER RESULT")
            print(result)

        # Test finance
        if "finance" in manager.sessions:

            result = await manager.call_tool(
                "finance",
                "convert_currency",
                {
                    "amount": 100,
                    "from_currency": "USD",
                    "to_currency": "INR"
                }
            )

            print("\nFINANCE RESULT")
            print(result)

        # Test database
        if "database" in manager.sessions:

            result = await manager.call_tool(
                "database",
                "search_customers",
                {
                    "query": "Rahul",
                    "limit": 10
                }
            )

            print("\nDATABASE RESULT")
            print(result)

    finally:

        await manager.disconnect_all()


if __name__ == "__main__":
    asyncio.run(main())
