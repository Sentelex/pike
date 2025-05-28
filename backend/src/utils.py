import langchain_core.tools as lcct

def tool_with_metadata(name: str, metadata: dict):
    def wrapper(func):
        tool = lcct.tool(name)(func)
        tool.metadata = metadata
        return tool
    return wrapper