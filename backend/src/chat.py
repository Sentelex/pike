from typing import Annotated, Sequence, Optional
import dotenv
import os
import pydantic as pdc
import uuid as u
import datetime as dt

import langchain_core.messages as lcm
import langgraph.graph.message as lgm
import langchain_google_genai as lcg
import langchain_openai as loai
import src.tools as tools


dotenv.load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key:
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
else:
    os.environ["OPENAI_API_KEY"] = ""

TOOL_LIST_LOOKUP = {
    "default": [
        tools.get_action_items,
        tools.parse_pdf,
        tools.get_stock_price,
        tools.parse_file,
        tools.parse_webpage,
        tools.summarize_text,
    ],
    "default_oai": [
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
        model="gemini-2.0-flash", google_api_key=google_api_key
    ),
    "default_oai": loai.ChatOpenAI(model="gpt-4o"),
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
    agent_id: str
    messages: Annotated[
        list[lcm.BaseMessage],
        pdc.Field(default_factory=list),
        lgm.add_messages
    ]
    name: str = "Chat"
    new_message: Optional[lcm.BaseMessage] = None
    opened: bool = True
    pinned: bool = False
    bookmarked: bool = False
    created: dt.datetime = pdc.Field(default_factory=dt.datetime.now)
    last_update: dt.datetime = pdc.Field(default_factory=dt.datetime.now)

    def model_post_init(self, __context: Optional[dict] = None) -> None:
        global CHAT_CACHE
        CHAT_CACHE[self.id] = self
