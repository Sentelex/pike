import langchain_core.tools as lcct
import fitz
import unicodedata


@lcct.tool
def parse_pdf(file_path: str) -> str:
    """
    Extracts and returns the full text content from a PDF file using PyMuPDF.

    Parameters:
    - file_path (str): Path to the PDF file.

    Returns:
    - str: Extracted text from the PDF.
    """
    try:
        with fitz.open(file_path) as doc:
            if doc.is_encrypted:
                doc.authenticate("")  # encrypted pdfs openable with no password

            text = "\n".join(page.get_text() for page in doc)
            # Normalize the text to NFC (Normalization Form C)
            normalized_text = unicodedata.normalize("NFC", text)
            return normalized_text.strip()

    except Exception as e:
        raise RuntimeError(f"Failed to parse PDF: {e}")
