import langchain_core.tools as lcct
import fitz
import unicodedata
from ..models import skill as sk


def get_pdf_attachment(id: str):
    """Mock: Return a fake PDF attachment."""
    pass


class PDFParserSkill(sk.Skill):
    name: str = "PDF Parser"
    description: str = (
        "Extract and return the full text content from PDF files using PyMuPDF"
    )
    icon: str = "📄"

    def parse_pdf(attachment_id: str) -> str:
        """
        Extract and return the full text content from a PDF file.

        Parameters:
        - attachment_id (str): UUID reference to the PDF file.

        Returns:
        - str: Extracted and normalized text content from the PDF.
        """
        # TODO: Implement get_pdf_attachment in a utility module
        attachment = None  # Placeholder for get_pdf_attachment(attachment_id)

        with fitz.open(stream=attachment, filetype="pdf") as doc:
            if doc.is_encrypted:
                doc.authenticate("")  # encrypted pdfs openable with no password

            text = "\n".join(page.get_text() for page in doc)
            normalized_text = unicodedata.normalize("NFC", text)
            return normalized_text.strip()

    tool: lcct.Tool = lcct.tool("PDF Parser")(parse_pdf)
