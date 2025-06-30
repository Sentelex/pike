import langchain_core.tools as lcct
import typing as t
from ..models import icon_process as ip
from ..models import skill as sk

# Candidate Icon:
# https://images.unsplash.com/photo-1662027008658-b615840c7deb?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dG9kbyUyMGljb258ZW58MHx8MHx8fDA%3D

class ActionItemSkill(sk.Skill):
    name: str = "Action Item Extractor"
    description: str = "Extract actionable items from text content"
    icon: str = ip.encode_icon_url_safe_utf8("check-mark-notepad-svgrepo-com.svg")

    get_action_items: t.ClassVar[lcct.StructuredTool]
    @lcct.tool((name.replace(" ", "_")))
    def get_action_items(text: str) -> str:
        """
        Extract actionable items from the provided text.

        Parameters:
        - text (str): The text content to analyze for action items.

        Returns:
        - str: List of extracted action items.
        """
        return "Action items content from the text (mocked)."

    tool: lcct.Tool = get_action_items
