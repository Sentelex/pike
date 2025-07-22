import backend.src.pike_tool as pt

@pt.pike_tool(display="Summarize Text", icon="flipped-book-svgrepo-com.svg")
def summarize_text(text: str) -> str:
    """Mock: Return a fake summary."""
    return "This is a summary of the text (mocked)."
