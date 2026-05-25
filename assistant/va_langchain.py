# valangchain.py

import os
import logging
from typing import List

from django.conf import settings
from django.db import transaction

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from .models import ChatSession, ChatMessage

logger = logging.getLogger(__name__)


# ==============================
# CONFIG
# ==============================
MAX_HISTORY = 20  # last N messages to keep
MODEL_NAME = "gemini-1.5-flash"


# ==============================
# GEMINI / LLM
# ==============================
def get_llm():
    """
    Initialize Gemini LLM.
    Expects GOOGLE_API_KEY in Django settings or env.
    """
    api_key = getattr(settings, "GOOGLE_API_KEY", None) or os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in settings or environment.")

    return ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        google_api_key=api_key,
        temperature=0.7,
    )


# ==============================
# SESSION HELPERS
# ==============================
def get_session(session_id: int) -> ChatSession:
    """
    Fetch ChatSession safely.
    """
    return ChatSession.objects.get(id=session_id)


def clear_session_memory(session_id: int):
    """
    Delete all messages for a session.
    Keeps ChatSession itself.
    """
    session = get_session(session_id)
    ChatMessage.objects.filter(session=session).delete()


# ==============================
# CHAT HISTORY
# ==============================
def load_chat_history(session: ChatSession) -> List:
    """
    Convert DB messages → LangChain message objects.
    """
    db_messages = (
        ChatMessage.objects
        .filter(session=session)
        .order_by("timestamp")[:MAX_HISTORY]
    )

    history = []

    for msg in db_messages:
        if msg.role == "user":
            history.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            history.append(AIMessage(content=msg.content))

    return history


def trim_old_history(session: ChatSession):
    """
    Keep only recent N messages.
    Prevent DB growth / token bloat.
    """
    ids = list(
        ChatMessage.objects
        .filter(session=session)
        .order_by("-timestamp")
        .values_list("id", flat=True)
    )

    if len(ids) > MAX_HISTORY:
        old_ids = ids[MAX_HISTORY:]
        ChatMessage.objects.filter(id__in=old_ids).delete()


# ==============================
# PROMPT / CHAIN
# ==============================
def build_prompt():
    """
    Prompt template for Nova.
    """
    return ChatPromptTemplate.from_messages([
        SystemMessage(
            content=(
                "You are Nova, a helpful AI assistant inside a Django app. "
                "Remember prior conversation context. "
                "Be clear, concise, and helpful."
            )
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])


# ==============================
# SAVE
# ==============================
@transaction.atomic
def save_messages(session: ChatSession, prompt: str, response: str):
    """
    Save user + assistant response.
    """
    ChatMessage.objects.create(
        session=session,
        role="user",
        content=prompt
    )

    ChatMessage.objects.create(
        session=session,
        role="assistant",
        content=response
    )


# ==============================
# MAIN ENTRYPOINT
# ==============================
def ask_nova(session_id: int, prompt: str) -> str:
    """
    Main function used by views.py

    Example:
        answer = ask_nova(chat_session.id, "Hello")
    """
    try:
        session = get_session(session_id)
        history = load_chat_history(session)
        llm = get_llm()
        prompt_template = build_prompt()

        chain = prompt_template | llm

        result = chain.invoke({
            "history": history,
            "input": prompt
        })

        response = result.content

        save_messages(session, prompt, response)
        trim_old_history(session)

        return response

    except ChatSession.DoesNotExist:
        logger.exception("Chat session not found.")
        return "Chat session not found."

    except Exception as e:
        logger.exception("Nova failed.")
        return f"Nova error: {str(e)}"