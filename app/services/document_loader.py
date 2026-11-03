from pathlib import Path

from docx import Document as DocxDocument

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader


def load_pdf(file_path : str) -> list[Document]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported.")

    loader = PyPDFLoader(str(path))

    documents = loader.load()

    for document in documents:
        document.metadata["source"] = path.name
        document.metadata["file_type"] = "pdf"

    return documents


def load_docx(file_path: str) -> list[Document]:

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if path.suffix.lower() != ".docx":
        raise ValueError("Only DOCX files are supported.")

    doc = DocxDocument(str(path))


    content = []

    # Extract Paragraphs
    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()

        if text:
            content.append(text)

    # Extract Tables
    for table in doc.tables:
        for row in table.rows:
            row_text = " | ".join(
                cell.text.strip() for cell in row.cells
            )

            if row_text.strip():
                content.append(row_text)

    extracted_text = "\n".join(content)

    document = Document(
        page_content = extracted_text,
        metadata = {
            "source" : path.name,
            "file_type" : "docx"
        }
    )

    return [document]


def load_document(file_path: str) -> list[Document]:

    path = Path(file_path)

    extension = path.suffix.lower()

    if extension == ".pdf":
        return load_pdf(str(path))

    elif extension == ".docx":
        return load_docx(str(path))

    else:
        raise ValueError(
            "Unsupported file format. Use PDF or DOCX"
        )
        
