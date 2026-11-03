from pathlib import Path

import pytest
from docx import Document as DocxDocument
from pypdf import PdfWriter

from app.services.document_loader import (
    load_pdf,
    load_docx,
    load_document
)


def test_load_docx(tmp_path):

    file_path = tmp_path / "sample.docx"

    doc = DocxDocument()
    doc.add_paragraph("This is a sample RAG document.")
    doc.save(file_path)

    documents = load_docx(str(file_path))

    assert len(documents) == 1
    assert "sample RAG document" in documents[0].page_content
    assert documents[0].metadata["source"] == "sample.docx"
    assert documents[0].metadata["file_type"] == "docx"


def test_load_pdf(tmp_path):

    file_path = tmp_path / "sample.pdf"

    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)

    with open(file_path, "wb") as file:
        writer.write(file)

    documents = load_pdf(str(file_path))

    assert len(documents) == 1
    assert documents[0].metadata["source"] == "sample.pdf"
    assert documents[0].metadata["file_type"] == "pdf"


def test_load_missing_file():

    with pytest.raises(FileNotFoundError):
        load_document("missing_document.pdf")


def test_unsupported_file(tmp_path):

    file_path = tmp_path / "sample.txt"
    file_path.write_text("Sample text")

    with pytest.raises(ValueError):
        load_document(str(file_path))


def test_invalid_pdf_extension(tmp_path):

    file_path = tmp_path / "sample.docx"
    file_path.write_text("Not a PDF")

    with pytest.raises(ValueError):
        load_pdf(str(file_path))


def test_invalid_docx_extension(tmp_path):

    file_path = tmp_path / "sample.pdf"
    file_path.write_text("Not a DOCX")

    with pytest.raises(ValueError):
        load_docx(str(file_path))