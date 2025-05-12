import json

# from typing import Callable, List
import langchain_core.messages as lcm
import langchain_core.runnables as lcr
import langgraph.graph as lgg

import src.state as st
import src.tools as tools
import langgraph.checkpoint.memory as lgcm


TOOL_LIST_LOOKUP = {
    "default": [
        tools.get_action_items,
        tools.parse_pdf,
        tools.get_stock_price,
        tools.parse_file,
        tools.parse_webpage,
        tools.summarize_text,
    ],
}


def tools_node(state: st.State, tools: list[callable]):
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


def assistant_node(state: st.State, model: lcr.RunnableConfig):
    system_prompt = lcm.SystemMessage(
        "You are a helpful assistant with tools at your disposal. If you can use a tool try to use a tool."
    )
    response = model.invoke([system_prompt] + state.messages)
    return {"messages": [response]}


def tool_condition(state: st.State):
    # Check if the last message is a tool call
    last_message = state.messages[-1]
    return "tools" if last_message.tool_calls else "end"


def add_new_message(state: st.StateFull) -> st.StateFull:
    return {"full_messages": [state.new_message]}


def truncate_history(s: st.StateFull, max_messages: int = 10) -> st.State:
    """
    Truncate the history of messages to the last max_messages.
    """
    if len(s.full_messages) >= max_messages:
        return {"messages": s.full_messages[-max_messages:]}
    else:
        return {"messages": s.full_messages}


def build_graph(model, graph_id: str) -> lgg.StateGraph:
    tools = TOOL_LIST_LOOKUP.get(graph_id, [])
    _model = model.bind_tools(tools)
    _graph = lgg.StateGraph(st.State)
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
