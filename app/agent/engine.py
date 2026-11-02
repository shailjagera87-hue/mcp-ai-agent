
from langchain.agents import create_agent
from langchain_groq import ChatGroq

from app.config.config import settings
from app.agent.prompts import SYSTEM_PROMPT
from app.agent.memory import ConversationMemory
from app.mcp_client.adapter import MCPToolAdapter


class MCPAIAgent:

    def __init__(self, agent, tools, memory):
        self.agent = agent
        self.tools = tools
        self.memory = memory

    @classmethod
    async def create(cls, mcp_manager):

        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is missing.")

        # Discover MCP tools.
        adapter = MCPToolAdapter(mcp_manager)
        tools = await adapter.build_tools()

        if not tools:
            raise RuntimeError("No MCP tools discovered.")

        # Initialize Groq.
        llm = ChatGroq(
            model=settings.GROQ_MODEL,
            temperature=0,
            api_key=settings.GROQ_API_KEY,
        )

        # Initialize conversation memory.
        memory = ConversationMemory()

        # Create agent with memory enabled.
        agent = create_agent(
            model=llm,
            tools=tools,
            system_prompt=SYSTEM_PROMPT,
            checkpointer=memory.checkpointer,
        )

        return cls(agent, tools, memory)

    async def chat(
        self,
        user_message: str,
        conversation_id: str,
    ) -> str:

        # Get memory configuration for this conversation.
        config = self.memory.get_config(conversation_id)

        # Invoke the agent with the current user message.
        result = await self.agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_message,
                    }
                ]
            },
            config=config,
        )

        # Extract the final response.
        final_message = result["messages"][-1]

        return final_message.content
