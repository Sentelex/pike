import langchain_core.messages as lc_messages
import uuid
from typing import Any, List, Optional, Union


class MockLLM:
    """
    Mock LLM that supports tools and responds with tool call results.
    """

    def __init__(self, responses: Optional[List[str]] = None):
        self.responses = responses or ["This is a mock response."]
        self.call_count = 0
        self.tools = []

    def bind_tools(self, tools):
        """Mock bind_tools method that stores tools for later use."""
        self.tools = tools
        return self

    def text_from_messages(self, input: str | list | dict,
                            search_keys: list | None = None) -> list[str]:
        expanded = [item for item in input]
        keep_expanding = True
        if search_keys is None:
            search_keys = ["text"]
        while keep_expanding:
            keep_expanding = False
            new_expanded = []
            for index in range(len(expanded)):
                if isinstance(expanded[index],str):
                    new_expanded.append(expanded[index])
                elif isinstance(expanded[index],lc_messages.BaseMessage):
                    new_expanded.append(expanded[index].content)
                    keep_expanding=True
                elif isinstance(expanded[index],list):
                    new_expanded.extend(expanded[index])
                    keep_expanding=True
                elif isinstance(expanded[index],dict):
                    new_expanded.extend([expanded[index].get(k,"") for k in search_keys])
                    keep_expanding=True
                else:
                    raise ValueError("Unsupported input type to MockLLM")
            expanded=new_expanded
        return expanded       


    def invoke(self,
               input: Union[str, List[lc_messages.BaseMessage]],
               **kwargs: Any) -> lc_messages.BaseMessage:
        """Mock invoke method that returns responses and simulates tool calls."""
        if type(input) not in [str, list, dict]:
            raise ValueError("Unsupported input type to MockLLM")
        input_text = " ".join(self.text_from_messages(input))
        
        response = self.responses[self.call_count % len(self.responses)]
        self.call_count += 1

        # Simulate tool call responses based on the input
        if "tool_calls" in kwargs:
            # If tool calls are included, simulate invoking the tools
            tool_calls = kwargs["tool_calls"]
            for tool_call in tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                for tool in self.tools:
                    if tool.name == tool_name:
                        result = tool.invoke(tool_args)
                        return lc_messages.ToolMessage(
                            content=result,
                            name=tool_name,
                            tool_call_id=tool_call["id"]
                        )
        if isinstance(response, str):
            return lc_messages.BaseMessage(content=response, type="text")
        elif isinstance(response, lc_messages.BaseMessage):
            response = response.copy()
            response.id = uuid.uuid4()
            return response

    def __repr__(self):
        return f"<MockLLM call_count={self.call_count}>"
