import pydantic as pyd
import user_spec as user
import chat_spec as chat
import agent_spec as agent
import bisect


class UserChat(pyd.BaseModel):
    """
    Map of users to the set of chats they have engaged in.
    """

    __root__: pyd.Dict[user.UserToken, pyd.Set[chat.ChatToken]]

    def __init__(self, data: pyd.Dict[user.UserToken, pyd.Set[chat.ChatToken]]):
        super().__init__(__root__=data)


class ChatByToken(pyd.BaseModel):
    """
    Map of ChatTokens to the associated ChatDescriptors.
    This map should always be 1:1
    """

    __root__: pyd.Dict[chat.ChatToken, chat.ChatDescriptor]

    def __init__(
        self,
        data: pyd.Set[chat.ChatTag],
    ):

        if isinstance(data, set):
            super().__init__(__root__={tag.token: tag.description for tag in data})
        else:
            raise TypeError(
                f"ERROR instantiating a {self.__class__.__name__}:\n"
                f"Expected a set of ChatTag values, but got {type(data).__name__} instead."
            )

def _build_dict_from_tags(tag_set: set[str,str])->dict[str, list[str]]:
    """
    Build the 1:many dictionaries in a generic way.
    """
    data_dict = {}
    for tag in tag_set:
        if tag.descriptor not in data_dict:
            data_dict[tag.descriptor] = [tag.token]
        else:
            # Use bisect to insert the token in sorted order
            bisect.insort(data_dict[tag.descriptor], tag.token)
    return data_dict

def _improper_input_error(classname: str, expected: str, received: str)->str:
    """
    Build the error message for improper input types.
    """
    return (
        f"ERROR instantiating a {classname}:\n"
        f"Expected a set of {expected} values, but got {received} instead."
    )

class ChatByDescriptor(pyd.BaseModel):
    """
    Map of ChatDescriptors to the associated (list of) ChatTokens.
    This map may be 1:many
    """

    __root__: pyd.Dict[chat.ChatDescriptor, pyd.List[chat.ChatToken]]

    def __init__(self, data: pyd.set[chat.ChatTag]):
        if isinstance(data, set):
            super().__init__(__root__=_build_dict_from_tags(data))
        else:
            raise TypeError(
                _improper_input_error(self.__class__.__name__, 'ChatToken'}:\n"
                f"Expected a set of chat.ChatToken values, but got {type(data).__name__} instead."
            )


class AgentByToken(pyd.BaseModel):
    """
    Map of AgentTokens to the associated AgentDescriptors.
    This map should always be 1:1
    """

    __root__: pyd.Dict[agent.AgentToken, agent.AgentDescriptor]

    def __init__(
        self,
        data: pyd.Set[agent.AgentTag],
    ):

        if isinstance(data, set):
            super().__init__(
                __root__={agent.AgentToken(token): token for token in data}
            )
        else:
            raise TypeError(
                f"ERROR instantiating a {self.__class__.__name__}:\n"
                f"Expected a set of AgentTag values, but got {type(data).__name__} instead."
            )


class AgentByDescriptor(pyd.BaseModel):
    """
    Map of AgentDescriptors to the associated (list of) AgentTokens.
    This map may be 1:many
    """
    __root__: pyd.Dict[agent.AgentDescriptor, pyd.List[agent.AgentToken]]

    def __init__(self, data: pyd.set[agent.AgentTag]):
        if isinstance(data, set):
            data_dict = {}
            for tag in data:
                if tag.description not in data_dict:
                    data_dict[tag.description] = [tag.token]
                else:
                    # Use bisect to insert the token in sorted order
                    bisect.insort(data_dict[tag.description], tag.token)
            super().__init__(__root__=data_dict)
        else:
            raise TypeError(
                f"ERROR instantiating a {self.__class__.__name__}:\n"
                f"Expected a set of agent.AgentToken values, but got {type(data).__name__} instead."
            )