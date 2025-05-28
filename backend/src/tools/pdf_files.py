import fitz
import unicodedata
import os
import uuid
import src.utils as ut


def get_pdf_attachment(id: str):
    pass


@ut.tool_with_metadata(
    name="PDF Parser",
    metadata={
            "uuid": str(uuid.uuid4()),
            "icon": "https://plus.unsplash.com/premium_photo-1677723530050-a1b18109fdd0?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8cGRmJTIwaWNvbnxlbnwwfHwwfHx8MA%3D%3D",
        }
)
def parse_pdf(attachment_id: str) -> str:
    """
    Extracts and returns the full text content from a PDF file using PyMuPDF.

    Parameters:
    - attachment_id (str): UUID reference to the PDF file.

    Returns:
    - str: Extracted text from the PDF.
    """
    attachment = get_pdf_attachment(attachment_id)

    # Fix: use stream=... and filetype='pdf'
    with fitz.open(stream=attachment, filetype="pdf") as doc:
        if doc.is_encrypted:
            doc.authenticate("")  # encrypted pdfs openable with no password

        text = "\n".join(page.get_text() for page in doc)
        normalized_text = unicodedata.normalize("NFC", text)
        return normalized_text.strip()
