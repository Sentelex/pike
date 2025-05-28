import uuid
import src.utils as ut


@ut.tool_with_metadata(
    name="Action Item Extractor",
    metadata={
            "uuid": str(uuid.uuid4()),
            "icon": "https://images.unsplash.com/photo-1662027008658-b615840c7deb?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dG9kbyUyMGljb258ZW58MHx8MHx8fDA%3D",
        }
)
def get_action_items(text: str) -> str:
    """Mock: Return fake action items content from text."""
    return "Action items content from the text (mocked)."
