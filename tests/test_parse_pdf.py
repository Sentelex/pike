import io
import base64
import pytest
from unittest.mock import patch
from reportlab.pdfgen import canvas

from src.tools.pdf_files import parse_pdf


def generate_test_pdf_bytes() -> bytes:
    """
    Generates a simple PDF in-memory and returns its binary content.
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, "This is a test PDF. Hello World!")
    c.save()
    buffer.seek(0)
    return buffer.read()


@pytest.fixture
def encoded_pdf_data():
    """
    Returns a base64-encoded string representing a small in-memory PDF file.
    """
    pdf_bytes = generate_test_pdf_bytes()
    return base64.b64encode(pdf_bytes).decode('utf-8')


@patch("src.tools.pdf_files.get_attachment")
def test_parse_pdf_reads_content(mock_get_attachment, encoded_pdf_data):
    # Decode base64 string to get binary content
    pdf_binary = base64.b64decode(encoded_pdf_data)
    mock_get_attachment.return_value = io.BytesIO(pdf_binary)

    content = parse_pdf("fake-uuid-1234")

    assert isinstance(content, str)
    assert "Hello World" in content
    assert "This is a test PDF" in content


@patch("src.tools.pdf_files.get_attachment")
def test_parse_pdf_invalid_attachment(mock_get_attachment):
    mock_get_attachment.side_effect = FileNotFoundError("Attachment not found")

    with pytest.raises(FileNotFoundError):
        parse_pdf("non-existent-uuid")
