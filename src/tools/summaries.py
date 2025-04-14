from langchain_core.tools import tool


@tool
def summarize_text(text: str) -> str:
    """Mock: Return a fake summary."""
    return "This is a summary of the text (mocked)."
