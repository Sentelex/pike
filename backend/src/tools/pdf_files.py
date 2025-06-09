import fitz
import unicodedata
import langchain_core.tools as lcct


def get_pdf_attachment(id: str):
    pass


@lcct.tool("PDF Parser")
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
