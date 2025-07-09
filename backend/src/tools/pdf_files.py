import langchain_core.tools as lcct
import fitz
import unicodedata
import typing as t
from ..models import icon_process as ip
from ..models import skill as sk


def get_pdf_attachment(id: str):
    """Mock: Return a fake PDF attachment."""
    pass


#  Candidate Icon:
#  https://plus.unsplash.com/premium_photo-1677723530050-a1b18109fdd0?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8cGRmJTIwaWNvbnxlbnwwfHwwfHx8MA%3D%3D

class PDFParserSkill(sk.Skill):
    name: str = "PDF Parser"
    description: str = "Extract and return the full text content from PDF files using PyMuPDF"
    icon: str = ip.encode_icon_url_safe_utf8("pdf-file-svgrepo-com.svg")

    parse_pdf: t.ClassVar[lcct.StructuredTool]
    @lcct.tool(name.replace(" ", "_"))
    def parse_pdf(attachment_id: str) -> str:
        """
        Extract and return the full text content from a PDF file.

        Parameters:
        - attachment_id (str): UUID reference to the PDF file.

        Returns:
        - str: Extracted and normalized text content from the PDF.
        """
        # TODO: Implement get_pdf_attachment in a utility module
        attachment = get_pdf_attachment(attachment_id)

        with fitz.open(stream=attachment, filetype="pdf") as doc:
            if doc.is_encrypted:
                doc.authenticate("")  # encrypted pdfs openable with no password

            text = "\n".join(page.get_text() for page in doc)
            normalized_text = unicodedata.normalize("NFC", text)
            return normalized_text.strip()

    tool: lcct.StructuredTool = parse_pdf
