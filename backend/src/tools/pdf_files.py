import fitz
import unicodedata
import src.pike_tool as pt
import pydantic as pdc

def get_pdf_attachment(id: str):
    pass


class ParsePDFArgs(pdc.BaseModel):
    pdf_file: str = pdc.Field(
        description="Unicode encoded binary content representing a PDF file from which text will be extracted."
    )


@pt.pike_tool(display="Extract PDF", 
              icon="pdf-file-svgrepo-com.svg",
              args_schema=ParsePDFArgs)
def parse_pdf(pdf_file: str) -> str:
    """
    Extracts and returns the full text content from a PDF file using PyMuPDF.

    Parameters:
    - attachment_id (str): UUID reference to the PDF file.

    Returns:
    - str: Extracted text from the PDF.
    """
    attachment = get_pdf_attachment(attachment_id)
    with fitz.open(stream=attachment, filetype="pdf") as doc:
        if doc.is_encrypted:
            doc.authenticate("")  # encrypted pdfs openable with no password

        text = "\n".join(page.get_text() for page in doc)
        normalized_text = unicodedata.normalize("NFC", text)
        return normalized_text.strip()
