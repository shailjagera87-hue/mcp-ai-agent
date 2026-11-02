
import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def test_finance_mcp():

    server_url = "http://127.0.0.1:8002/mcp"

    async with streamablehttp_client(server_url) as (
        read_stream,
        write_stream,
        _,
    ):
        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            await session.initialize()

            # Discover available tools
            tools = await session.list_tools()

            print("\nAvailable Finance MCP Tools:")

            for tool in tools.tools:
                print(f"- {tool.name}")

            # Test currency conversion
            print("\nTesting Currency Conversion...")

            result = await session.call_tool(
                "convert_currency",
                arguments={
                    "amount": 100,
                    "from_currency": "USD",
                    "to_currency": "INR",
                },
            )

            print("\nConversion Result:")
            print(result)

            # Test exchange rate
            print("\nTesting Exchange Rate...")

            rate_result = await session.call_tool(
                "get_exchange_rate",
                arguments={
                    "from_currency": "USD",
                    "to_currency": "INR",
                },
            )

            print("\nExchange Rate Result:")
            print(rate_result)


if __name__ == "__main__":
    asyncio.run(test_finance_mcp())
