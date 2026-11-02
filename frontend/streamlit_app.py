
import uuid
import requests
import streamlit as st


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="MCP AI Agent",
    page_icon="🤖",
    layout="wide",
)

API_BASE_URL = "http://127.0.0.1:8000"


# -----------------------------
# Session State
# -----------------------------

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# API Functions
# -----------------------------

def check_backend():
    try:
        response = requests.get(
            f"{API_BASE_URL}/health",
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException:
        return None


def get_available_tools():
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/tools",
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException:
        return []


def send_message(message):
    payload = {
        "message": message,
        "conversation_id": st.session_state.conversation_id,
    }

    response = requests.post(
        f"{API_BASE_URL}/api/chat",
        json=payload,
        timeout=120,
    )

    response.raise_for_status()

    return response.json()


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.title("🤖 MCP AI Agent")

    st.caption("Multi-tool AI assistant")

    st.divider()

    st.subheader("Backend Status")

    health = check_backend()

    if health and health.get("agent_ready"):
        st.success("Backend Connected")

        for server in health.get("connected_servers", []):
            st.write(f"🟢 {server.title()} MCP")

    else:
        st.error("Backend Unavailable")

    st.divider()

    st.subheader("Available MCP Tools")

    tools = get_available_tools()

    if tools:
        for tool in tools:
            with st.expander(tool["name"]):
                st.write(tool["description"])
    else:
        st.info("No tools available.")

    st.divider()

    if st.button("➕ New Conversation", use_container_width=True):
        st.session_state.conversation_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

    st.caption(
        f"Conversation ID: "
        f"{st.session_state.conversation_id[:8]}..."
    )


# -----------------------------
# Main Chat Interface
# -----------------------------

st.title("MCP AI Assistant")

st.write(
    "Ask questions about weather, currency conversion, "
    "exchange rates, and customer information."
)

st.divider()


# Display chat history.

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input.

user_input = st.chat_input("Ask your AI assistant...")

if user_input:

    # Display and store user message.
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Call FastAPI.
    with st.chat_message("assistant"):

        with st.spinner("AI agent is thinking..."):

            try:
                result = send_message(user_input)

                answer = result["response"]

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

            except requests.RequestException as error:

                answer = (
                    "Unable to communicate with the AI backend. "
                    "Please check that FastAPI is running."
                )

                st.error(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

                st.caption(str(error))

            except Exception as error:

                answer = "An unexpected error occurred."

                st.error(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

                st.caption(str(error))
