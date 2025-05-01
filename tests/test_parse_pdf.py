import io
import base64
import pytest
from reportlab.pdfgen import canvas as pdf_canvas

import src.tools.pdf_files as pf


@pytest.fixture
def generate_test_pdf_bytes() -> str:
    """
    Generates a simple PDF in-memory and returns its base64-encoded string.
    """
    buffer = io.BytesIO()
    c = pdf_canvas.Canvas(buffer)
    c.drawString(100, 750, "This is a test PDF. Hello World!")
    c.save()
    buffer.seek(0)
    pdf_bytes = buffer.read()
    return base64.b64encode(pdf_bytes).decode('utf-8')


def test_parse_pdf_reads_content(monkeypatch, generate_test_pdf_bytes):
    pdf_binary = base64.b64decode(generate_test_pdf_bytes)
    monkeypatch.setattr(pf, "get_attachment", lambda _: io.BytesIO(pdf_binary))

    content = pf.parse_pdf("fake-uuid-1234")

    assert isinstance(content, str)
    assert "Hello World" in content
    assert "This is a test PDF" in content


def test_parse_pdf_invalid_attachment(monkeypatch):
    monkeypatch.setattr(pf, "get_attachment", lambda _: (_ for _ in ()).throw(FileNotFoundError("Attachment not found")))

    with pytest.raises(FileNotFoundError):
        pf.parse_pdf("non-existent-uuid")
