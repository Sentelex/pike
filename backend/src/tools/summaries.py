import uuid
import src.utils as ut


@ut.tool_with_metadata(
    name="Text Summarizer",
    metadata={
            "uuid": str(uuid.uuid4()),
            "icon": "https://images.unsplash.com/photo-1705490020987-b4565b36c04d?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fHN1bW1hcml6ZXIlMjBpY29ufGVufDB8fDB8fHww",
        }
)
def summarize_text(text: str) -> str:
    """Mock: Return a fake summary."""
    return "This is a summary of the text (mocked)."
