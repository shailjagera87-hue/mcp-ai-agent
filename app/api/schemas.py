
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=5000,
        description="User's message to the AI agent",
    )

    conversation_id: str = Field(
        min_length=1,
        max_length=100,
        description="Unique ID for the conversation",
    )


class ChatResponse(BaseModel):
    conversation_id: str
    response: str


class ToolInfo(BaseModel):
    name: str
    description: str


class HealthResponse(BaseModel):
    status: str
    agent_ready: bool
    connected_servers: list[str]
