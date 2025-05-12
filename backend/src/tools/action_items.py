import src.pike_tool as pt
import pydantic as pdc


class ExtractActionItemsArgs(pdc.BaseModel):
    text: str = pdc.Field(
        description="Extract actionable items from user supplied text.")


@pt.pike_tool(display="Extract Action Items", 
              icon="check-mark-notepad-svgrepo-com.svg",
              args_schema=ExtractActionItemsArgs)
def get_action_items(text: str) -> str:
    """Mock: Return fake action items content from text."""
    return "Action items content from the text (mocked)."
