import langchain_core.tools as lcct
from ..models import skill as sk


class TextSummarizerSkill(sk.Skill):
    name: str = "Text Summarizer"
    description: str = "Generate concise summaries of text content"
    icon: str = "📋"

    def summarize_text(text: str) -> str:
        """
        Mock: Return a fake summary.
        """
        return "This is a summary of the text (mocked)."

    tool: lcct.Tool = lcct.tool(name.replace(" ","_"))(summarize_text)
