
from langgraph.checkpoint.memory import InMemorySaver


class ConversationMemory:

    def __init__(self):
        # In-memory conversation checkpoint storage.
        self.checkpointer = InMemorySaver()

    def get_config(self, conversation_id: str) -> dict:
        """
        Return the configuration for a conversation.

        The same conversation_id loads the previous
        conversation history.
        """

        if not conversation_id or not conversation_id.strip():
            raise ValueError("conversation_id cannot be empty")

        return {
            "configurable": {
                "thread_id": conversation_id
            }
        }
