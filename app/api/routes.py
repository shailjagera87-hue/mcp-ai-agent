
import logging

from fastapi import APIRouter, HTTPException, Request

from app.api.schemas import (
    ChatRequest,
    ChatResponse,
    ToolInfo,
    HealthResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check(request: Request):

    agent = getattr(request.app.state, "agent", None)
    manager = getattr(request.app.state, "mcp_manager", None)

    connected_servers = (
        list(manager.sessions.keys()) if manager else []
    )

    return HealthResponse(
        status="healthy" if agent else "initializing",
        agent_ready=agent is not None,
        connected_servers=connected_servers,
    )


@router.get("/api/tools", response_model=list[ToolInfo])
async def get_tools(request: Request):

    agent = getattr(request.app.state, "agent", None)

    if agent is None:
        raise HTTPException(
            status_code=503,
            detail="AI agent is not ready.",
        )

    return [
        ToolInfo(
            name=tool.name,
            description=tool.description,
        )
        for tool in agent.tools
    ]


@router.post("/api/chat", response_model=ChatResponse)
async def chat(request_data: ChatRequest, request: Request):

    agent = getattr(request.app.state, "agent", None)

    if agent is None:
        raise HTTPException(
            status_code=503,
            detail="AI agent is not available.",
        )

    try:
        response = await agent.chat(
            user_message=request_data.message,
            conversation_id=request_data.conversation_id,
        )

        return ChatResponse(
            conversation_id=request_data.conversation_id,
            response=response,
        )

    except Exception:
        logger.exception("AI agent request failed")

        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your request.",
        )
