import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def test_server(name, url):

    print(f"\nTesting {name}...")

    try:
        async with streamablehttp_client(url) as (
            read_stream,
            write_stream,
            get_session_id
        ):

            async with ClientSession(
                read_stream,
                write_stream
            ) as session:

                await session.initialize()

                result = await session.list_tools()

                print(f"{name}: CONNECTED")

                for tool in result.tools:
                    print("Tool:", tool.name)

    except Exception as error:

        print(f"{name}: FAILED")
        print(type(error).__name__, str(error))


async def main():

    await test_server(
        "Weather",
        "http://127.0.0.1:8001/mcp"
    )

    await test_server(
        "Finance",
        "http://127.0.0.1:8002/mcp"
    )

    await test_server(
        "Database",
        "http://127.0.0.1:8003/mcp"
    )


if __name__ == "__main__":
    asyncio.run(main())