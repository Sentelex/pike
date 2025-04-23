import typing as t
import pydantic as pyd
import backend.uuid_hierarchy as uh

ChatToken = t.NewType("ChatToken", uh.SafeUUID)
ChatDescriptor = t.NewType("ChatDescriptor", str)


class ChatTag(pyd.BaseModel):
    """
    Tag for identifying a unique chat.
    """

    token: ChatToken
    description: ChatDescriptor
