import langchain_core.tools as lcct
from ..models import skill as sk


class ActionItemSkill(sk.Skill):
    name: str = "Action Item Extractor"
    description: str = "Extract actionable items from text content"
    icon: str = "✅"

    def get_action_items(text: str) -> str:
        """
        Extract actionable items from the provided text.

        Parameters:
        - text (str): The text content to analyze for action items.

        Returns:
        - str: List of extracted action items.
        """
        return "Action items content from the text (mocked)."

    tool: lcct.Tool = lcct.tool(name.replace(" ","_"))(get_action_items)
