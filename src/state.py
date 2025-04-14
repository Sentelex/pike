from typing import Annotated, Sequence, Optional
import langchain_core.messages as lcm
import langgraph.graph.message as lgm
import pydantic as pdc


class StateFull(pdc.BaseModel):
    new_message: lcm.BaseMessage
    full_messages: Optional[Annotated[Sequence[lcm.BaseMessage],
                                      lgm.add_messages]] = []
    attachment: Optional[str] = None  # Default to None for optional fields
    graph_id: Optional[str] = None  # Default to None for optional fields


class State(StateFull):
    """
    State class for managing the state of the graph.
    Inherits from StateFull and adds a messages field.
    """
    messages: Annotated[Sequence[lcm.BaseMessage], lgm.add_messages]
