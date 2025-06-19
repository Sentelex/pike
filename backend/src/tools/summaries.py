import langchain_core.tools as lcct
from ..models import icon_process as ip
from ..models import skill as sk

#  Candidate Icon:
#  https://images.unsplash.com/photo-1705490020987-b4565b36c04d?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fHN1bW1hcml6ZXIlMjBpY29ufGVufDB8fDB8fHww

class TextSummarizerSkill(sk.Skill):
    name: str = "Text Summarizer"
    description: str = "Generate concise summaries of text content"
    icon: str = ip.encode_icon_url_safe_utf8("flipped-book-svgrepo-com.svg")

    def summarize_text(text: str) -> str:
        """
        Mock: Return a fake summary.
        """
        return "This is a summary of the text (mocked)."

    tool: lcct.Tool = lcct.tool(name.replace(" ","_"))(summarize_text)
