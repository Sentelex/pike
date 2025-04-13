from typing import Annotated, Sequence, TypedDict, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    attachment: Optional[str]  # For attachments like PDFs
    graph_id: Optional[str]  # To support multiple graphs if needed
