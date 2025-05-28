from typing import Annotated, Sequence, Optional
import dotenv
import os
import pydantic as pdc
import uuid as u
import datetime as dt

import langchain_core.messages as lcm
import langgraph.graph.message as lgm
import langchain_google_genai as lcg
import langgraph.prebuilt as lgp
import src.tools as tools


dotenv.load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

TOOL_LIST_LOOKUP = {
    "default": [
        tools.get_action_items,
        tools.parse_pdf,
        tools.get_stock_price,
        tools.parse_file,
        tools.parse_webpage,
        tools.summarize_text,
    ],
}

CHAT_CACHE: dict[u.UUID, 'Chat'] = {}
ATTACHMENT_CACHE: dict[str, str] = {}
AGENT_MODEL_LOOKUP = {
    "default": lcg.ChatGoogleGenerativeAI(
        model="gemini-2.0-flash", google_api_key=api_key
    ),
}
AGENT_CACHE = {}


class Chat(pdc.BaseModel):
    new_message: lcm.BaseMessage
    messages: Annotated[
        list[lcm.BaseMessage],
        pdc.Field(default_factory=list),
        lgm.add_messages
    ]
    attachment: Optional[str] = None  # Default to None for optional fields
    graph_id: Optional[str] = None  # Default to None for optional fields
    id: u.UUID
    agent_id: u.UUID
    name: str = "Chat"
    created: dt.datetime = pdc.Field(default_factory=dt.datetime.now)
    last_update: dt.datetime = pdc.Field(default_factory=dt.datetime.now)
    opened: bool = True
    pinned: bool = False
    bookmarked: bool = False


def get_response(chat_id: u.UUID, attachment: str) -> dict:
    """
    Converts a Chat object to a dictionary suitable for API response.
    """
    if chat_id not in CHAT_CACHE:
        raise ValueError(f"Chat with ID {chat_id} not found.")
    chat = CHAT_CACHE[chat_id]
    if attachment is not None:
        attachment_id = u.uuid4()
        ATTACHMENT_CACHE[attachment_id] = attachment
        CHAT_CACHE[chat.id].attachment = attachment_id
    if chat.agent_id not in AGENT_CACHE:
        model = AGENT_MODEL_LOOKUP.get(
            chat.agent_id, AGENT_MODEL_LOOKUP["default"])
        agent = lgp.create_react_agent(
            model=model,
            tools=TOOL_LIST_LOOKUP.get(
                chat.agent_id, TOOL_LIST_LOOKUP["default"]),
        )
        AGENT_CACHE[chat.agent_id] = agent
    else:
        agent = AGENT_CACHE[chat.agent_id]
    chat = agent.invoke(chat)
    chat.last_update = dt.datetime.now()
    CHAT_CACHE[chat.id] = chat
    return CHAT_CACHE[chat.id].messages[-1]
