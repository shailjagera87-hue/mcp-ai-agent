
import asyncio

from app.mcp_client.manager import MCPClientManager
from app.agent.engine import MCPAIAgent


async def main():

    async with MCPClientManager() as manager:

        print("MCP servers connected.")

        ai_agent = await MCPAIAgent.create(manager)

        print("\nAvailable tools:")

        for tool in ai_agent.tools:
            print(f"- {tool.name}")

        # One ID represents one conversation.
        conversation_id = "test-conversation-001"

        print("\nAI Agent with conversation memory is ready!")

        while True:

            question = input("\nYou: ").strip()

            if question.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break

            if not question:
                continue

            try:
                response = await ai_agent.chat(
                    user_message=question,
                    conversation_id=conversation_id,
                )

                print(f"\nAI Agent: {response}")

            except Exception as error:
                print(f"\nError: {error}")


if __name__ == "__main__":
    asyncio.run(main())
