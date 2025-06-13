from typing import Annotated, Optional
import pydantic as pdc
import uuid as u
import datetime as dt

import langchain_core.messages as lcm
import langgraph.graph.message as lgm

global CHAT_CACHE
global ATTACHMENT_CACHE
CHAT_CACHE: dict[u.UUID, 'Chat'] = {}
ATTACHMENT_CACHE: dict[str, str] = {}


class ChatInput(pdc.BaseModel):
    message: str
    attachment: dict | None = None


class Chat(pdc.BaseModel):
    id: u.UUID
    agent_id: u.UUID
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
