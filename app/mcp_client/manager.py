import logging
from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from app.config.config import settings

logger = logging.getLogger(__name__)


class MCPClientManager:

    def __init__(self):
        self.sessions = {}
        self.exit_stack = None

    async def __aenter__(self):
        self.exit_stack = AsyncExitStack()
        await self.exit_stack.__aenter__()

        try:
            await self.connect_all()
            return self
        except BaseException:
            await self.exit_stack.aclose()
            raise

    async def __aexit__(self, exc_type, exc, tb):
        self.sessions.clear()
        if self.exit_stack:
            await self.exit_stack.__aexit__(exc_type, exc, tb)
            self.exit_stack = None

    async def connect_to_server(self, server_name, server_url):
        if self.exit_stack is None:
            raise RuntimeError("Use MCPClientManager inside 'async with'.")

        read_stream, write_stream, _ = (
            await self.exit_stack.enter_async_context(
                streamablehttp_client(server_url)
            )
        )

        session = await self.exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )

        await session.initialize()
        tools = await session.list_tools()

        self.sessions[server_name] = session

        logger.info(
            "Connected to %s. Discovered %d tools.",
            server_name,
            len(tools.tools),
        )

        return tools.tools

    async def connect_all(self):
        results = {}

        for name, url in settings.MCP_SERVERS.items():
            try:
                tools = await self.connect_to_server(name, url)

                results[name] = {
                    "connected": True,
                    "tools": tools,
                }

            except Exception as error:
                logger.exception("Failed to connect to %s", name)

                results[name] = {
                    "connected": False,
                    "error": str(error),
                }

        return results

    async def call_tool(self, server_name, tool_name, arguments):
        session = self.sessions.get(server_name)

        if session is None:
            raise ValueError(f"{server_name} is not connected.")

        result = await session.call_tool(
            tool_name,
            arguments=arguments,
        )

        if result.isError:
            raise RuntimeError(f"MCP tool failed: {result}")

        return result