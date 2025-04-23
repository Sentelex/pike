import typing as t
import uuid_hierarchy as uh
import pydantic as pyd

AgentToken = t.NewType("AgentToken", uh.SafeUUID)
AgentDescriptor = t.NewType("AgentDescriptor", str)


class AgentTag(pyd.BaseModel):
    """
    Tag for identifying a unique agent.
    """

    token: AgentToken
    description: AgentDescriptor
