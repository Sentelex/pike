import typing as t
import pydantic as pyd
import uuid_hierarchy as uh

UserToken = t.NewType("UserToken", str)
UserName = t.NewType("UserName", str)


class UserTag(pyd.BaseModel):
    """
    Tag for identifying a unique user.
    """

    token: UserToken
    name: UserName
