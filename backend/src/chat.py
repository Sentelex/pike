from typing import Annotated, Sequence, Optional
import dotenv
import os
import pydantic as pdc
import uuid as u
import datetime as dt

import langchain_core.messages as lcm
import langgraph.graph.message as lgm
import langchain_google_genai as lcg
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
AGENT_MODEL_LOOKUP = {
    "default": lcg.ChatGoogleGenerativeAI(
        model="gemini-2.0-flash", google_api_key=api_key
    ),
}
global CHAT_CACHE
global ATTACHMENT_CACHE
global AGENT_CACHE
CHAT_CACHE: dict[u.UUID, 'Chat'] = {}
ATTACHMENT_CACHE: dict[str, str] = {}
AGENT_CACHE: dict[u.UUID, 'Agent'] = {}


class ChatInput(pdc.BaseModel):
    message: str
    attachment: dict | None = None


class Chat(pdc.BaseModel):
    id: u.UUID
    agent_id: u.UUID
    created: dt.datetime = pdc.Field(default_factory=dt.datetime.now)
    last_update: dt.datetime = pdc.Field(default_factory=dt.datetime.now)

    opened: bool = True
    pinned: bool = False
    bookmarked: bool = False

    name: str = "Chat"

    new_message: Optional[lcm.BaseMessage] = None
    messages: Annotated[
        list[lcm.BaseMessage],
        pdc.Field(default_factory=list),
        lgm.add_messages
    ]

