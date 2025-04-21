import os
import tempfile
import pytest
from reportlab.pdfgen import canvas

from src.tools.pdf_files import parse_pdf


@pytest.fixture
def dummy_pdf_file():
    """
    Creates a temporary PDF file with known content for testing.
    Cleans up the file after use.
    """
    fd, path = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)

    test_text = "This is a test PDF. Hello World!"
    c = canvas.Canvas(path)
    c.drawString(100, 750, test_text)
    c.save()

    yield path

    os.remove(path)


def test_parse_pdf_reads_content(dummy_pdf_file):
    content = parse_pdf(dummy_pdf_file)
    assert isinstance(content, str)
    assert "Hello World" in content
    assert "This is a test PDF" in content


def test_parse_pdf_invalid_path():
    with pytest.raises(FileNotFoundError):
        parse_pdf("non_existent_file.pdf")
