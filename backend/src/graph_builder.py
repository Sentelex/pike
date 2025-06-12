import json
import uuid as u
import datetime as dt
import pydantic as pdc
from typing import Sequence, Optional

import langchain_core.messages as lcm
import langchain_core.runnables as lcr
import langgraph.graph as lgg

import src.tools as tools
import src.chat as ct

TOOL_LIST_LOOKUP = {
    "default": [
        tools.get_action_items,
        tools.parse_pdf,
        tools.get_stock_price,
        tools.parse_file,
        tools.parse_webpage,
        tools.summarize_text,
    ]
}

global AGENT_CACHE
AGENT_CACHE: dict[u.UUID, 'Agent'] = {}


class AgentConfig(pdc.BaseModel):
    name: str
    description: str | None = None
    model: str | None = None
    tools: Sequence[str] = pdc.Field(default_factory=list)


class Agent(pdc.BaseModel):
    id: u.UUID
    name: str
    description: str | None = None
    tools: list
    model: object
    graph: object = None

    def model_post_init(self, __context: Optional[dict] = None) -> None:
        if len(self.tools) == 0:
            self.tools = TOOL_LIST_LOOKUP['default']
        self.graph = build_graph(self.model, self.tools)

    def invoke(self, state: ct.Chat) -> dict:
        """
        Invoke the agent's graph with the current chat state.
        """
        if not self.graph:
            raise ValueError("Graph is not initialized.")
        return self.graph.invoke(state)


def tools_node(state: ct.Chat, tools: list[callable]):
    tools_by_name = {tool.name: tool for tool in tools}
    outputs = []
    # Iterate through the tool calls in the last message of the state
    for tool_call in state.messages[-1].tool_calls:
        tool_result = tools_by_name[tool_call["name"]].invoke(
            tool_call["args"])
        outputs.append(
            lcm.ToolMessage(
                content=json.dumps(tool_result),
                name=tool_call["name"],
                tool_call_id=tool_call["id"],
            )
        )
    return {"messages": outputs}


def assistant_node(state: ct.Chat, model: lcr.RunnableConfig):
    system_prompt = lcm.SystemMessage(
        "You are a helpful assistant with tools at your disposal. If you can use a tool try to use a tool."
    )
    response = model.invoke([system_prompt] + state.messages)
    return {"messages": [response]}


def tool_condition(state: ct.Chat):
    # Check if the last message is a tool call
    last_message = state.messages[-1]
    return "tools" if last_message.tool_calls else "end"


def add_new_message(state: ct.Chat) -> ct.Chat:
    return {"messages": [state.new_message]}


def truncate_history(s: ct.Chat, max_messages: int = 10) -> ct.Chat:
    """
    Truncate the history of messages to the last max_messages.
    """
    if len(s.messages) >= max_messages:
        return {"messages": s.messages[-max_messages:]}
    else:
        return {"messages": s.messages}


def build_graph(model, tools) -> lgg.StateGraph:
    _model = model.bind_tools(tools)
    _graph = lgg.StateGraph(ct.Chat)
    _graph.add_node("message", add_new_message)
    _graph.add_node("truncate_history",
                    lambda s: truncate_history(s, max_messages=10))
    _graph.add_node("agent", lambda s: assistant_node(s, model=_model))
    _graph.add_node("tools", lambda s: tools_node(s, tools=tools))
    _graph.set_entry_point("message")
    _graph.add_edge("message", "truncate_history")
    _graph.add_edge("truncate_history", "agent")
    _graph.add_conditional_edges(
        "agent", tool_condition, {"tools": "tools", "end": lgg.END}
    )
    _graph.add_edge("tools", "agent")
    return _graph.compile()


def get_response(chat_id: u.UUID, input: ct.ChatInput) -> lcm.BaseMessage:
    """
    Converts a Chat object to a dictionary suitable for API response.
    """
    if chat_id not in ct.CHAT_CACHE:
        raise ValueError(f"Chat with ID {chat_id} not found.")

    message_content = []
    additional_kwargs = {}
    if input.message:
        message_content.append({"type": "text", "text": input.message})
    if input.attachment:
        additional_kwargs = additional_kwargs | {"attachment_id": u.uuid(4)}
        message_content.append(input.attachment)
    message = lcm.HumanMessage(
        content=message_content,
        additional_kwargs=additional_kwargs
    )

    chat = ct.CHAT_CACHE[chat_id]
    chat.new_message = message

    if chat.agent_id not in AGENT_CACHE:
        model = ct.MODEL_INTERFACE.get(
            chat.agent_id, ct.MODEL_INTERFACE["default"])
        agent = build_graph(
            model=model,
            tools=TOOL_LIST_LOOKUP.get(
                chat.agent_id, TOOL_LIST_LOOKUP["default"]),
        )
        AGENT_CACHE[chat.agent_id] = agent
    else:
        agent = AGENT_CACHE[chat.agent_id]
    chat = ct.Chat(**agent.invoke(chat))
    chat.last_update = dt.datetime.now()
    ct.CHAT_CACHE[chat.id] = chat
    return ct.CHAT_CACHE[chat.id].messages[-1]
