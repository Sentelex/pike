import pydantic as pyd
import uuid as u
import datetime as dt
import typing as t
import json

import langchain_core.messages as lcm
import langgraph.graph.message as lggm


class Chat(pyd.BaseModel):
    """
    Chat specifiers and data for interaction with an agentic chat instance.
    """
    id: u.UUID
    agent: u.UUID
    user: u.UUID
    name: str = f"Chat"
    created: dt.datetime = dt.datetime.now()
    last_update: dt.datetime = dt.datetime.now()
    opened: bool = True
    pinned: bool = False
    bookmarked: bool = False
    messages: t.Annotated[list[lcm.BaseMessage],lggm.add_messages]


