import json
from typing import Callable, List
from langchain_core.messages import ToolMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END
from state import State


def build_default_graph(model, tools: List[Callable], graph_id: str = "default"):
    tools_by_name = {tool.name: tool for tool in tools}

    # Define the tool node that handles tool calls in the graph
    def tool_node(state: State):
        outputs = []
        # Iterate through the tool calls in the last message of the state
        for tool_call in state["messages"][-1].tool_calls:
            # Invoke the appropriate tool and capture the result
            tool_result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])

            # Create a new ToolMessage with the tool result and append it to outputs
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        # Return the new messages (tool results) to update the state
        return {"messages": outputs}

    def call_model(state: State, config: RunnableConfig):
        system_prompt = SystemMessage(
            f"You are in the '{state.get('graph_id', 'default')}' graph. Respond helpfully!"
        )
        response = model.invoke([system_prompt] + state["messages"], config)
        # Return the model's response as part of the updated state
        return {"messages": [response]}

    def should_continue(state: State):
        last_message = state["messages"][-1]
        # If the last message includes tool calls, continue; otherwise, end
        return "continue" if last_message.tool_calls else "end"

    workflow = StateGraph(State)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", should_continue, {"continue": "tools", "end": END})
    workflow.add_edge("tools", "agent")

    return workflow.compile()
