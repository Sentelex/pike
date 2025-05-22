import pydantic as pyd
import uuid as u
import datetime as dt
import typing as t
import json

import langchain_core.messages as lcm
import langgraph.graph.message as lggm

class ChatData(pyd.BaseModel):
    """
    Relevant information about a specific chat for frontend and backend.
    """
    id: u.UUID
    agent: u.UUID
    user: u.UUID
    name: str
    created: dt.datetime
    last_update: dt.datetime

class ChatStatus(pyd.BaseModel):
    """
    Frontend status of a chat.
    """
    isOpen: bool
    isPinned: bool
    isBookmarked: bool

class ChatHistory(pyd.BaseModel):
    """
    Message history of a chat.
    """
    messages: t.Annotated[list[lcm.BaseMessage],lggm.add_messages]

class Chat(pyd.BaseModel):
    """
    A chat with an agentic chat model.
    """
    data: ChatData
    status: ChatStatus
    history: ChatHistory

    def interface_be2fe(self) -> dict:
        """
        Dumps the chat interface for the frontend.
        """
        data = data = {
                "chatId": str(self.data.id),
                "chatName": self.data.name,
                "isOpen": self.status.isOpen,
                "isPinned": self.status.isPinned,
                "isBookmarked": self.status.isBookmarked,
                "createdAt": self.data.created.isoformat(),
                "updatedAt": self.data.last_update.isoformat(),
                "agentId": str(self.data.agent)
            }
        return json.dumps(data, indent=4)
    
    def history_be2fe(self) -> dict:
        """
        Dumps the chat history for the frontend.
        """
        fields = ["content", "additional_kwargs", "type"]
        data = { "messages": 
            [ {field : getattr(msg, field, None) for field in fields}   
                for msg in self.history.messages]
            }        
        return json.dumps(data, indent=4)
    
    

if __name__ == "__main__":
    status = ChatStatus(isOpen=True, isPinned=False, isBookmarked=True)
    history = ChatHistory(messages=[lcm.HumanMessage(content="Hello"),lcm.AIMessage(content="Hi there!")])
    data = ChatData(id=u.uuid4(), agent=u.uuid4(), user=u.uuid4(), name="Test Chat", created=dt.datetime.now(), last_update=dt.datetime.now())

    chat = Chat(data=data, status=status, history=history)
    print(chat.model_dump_json(indent=4, include={'status':True, 'data':['id', 'name', 'created', 'last_update']}))
    print(chat.interface_be2fe())
    print(chat.history_be2fe())