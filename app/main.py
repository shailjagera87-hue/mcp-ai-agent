
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.agent.engine import MCPAIAgent
from app.mcp_client.manager import MCPClientManager
from app.config.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):

    manager = MCPClientManager()

    # Start MCP connections.
    await manager.__aenter__()

    try:
        # Ensure every configured MCP server connected.
        expected_servers = set(settings.MCP_SERVERS.keys())
        connected_servers = set(manager.sessions.keys())

        missing_servers = expected_servers - connected_servers

        if missing_servers:
            raise RuntimeError(
                f"Unable to connect to MCP servers: {missing_servers}"
            )

        logger.info("All MCP servers connected.")

        # Initialize LangChain agent.
        agent = await MCPAIAgent.create(manager)

        app.state.mcp_manager = manager
        app.state.agent = agent

        logger.info("LangChain AI agent initialized.")

        yield

    finally:
        # Close MCP connections when FastAPI stops.
        await manager.__aexit__(None, None, None)

        logger.info("MCP connections closed.")


app = FastAPI(
    title="MCP AI Agent API",
    description="AI agent with multiple MCP server integrations",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)
