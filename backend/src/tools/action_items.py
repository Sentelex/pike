import backend.src.pike_tool as pt

@pt.pike_tool(display="Extract Action Items", icon="check-mark-notepad-svgrepo-com.svg")
def get_action_items(text: str) -> str:
    """Mock: Return fake action items content from text."""
    return "Action items content from the text (mocked)."
