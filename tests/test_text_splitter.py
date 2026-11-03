from langchain_core.documents import Document

from app.services.text_splitter import split_documents


def test_split_document(sample_text):

    document = Document(
        page_content=sample_text,
        metadata={"source": "sample.pdf", "page": 0}
    )

    chunks = split_documents([document])

    assert len(chunks) >= 1

    for chunk in chunks:
        assert len(chunk.page_content) <= 1000


def test_metadata_preservation(sample_text):

    document = Document(
        page_content=sample_text,
        metadata={"source": "sample.pdf", "file_type": "pdf"}
    )

    chunks = split_documents([document])

    for chunk in chunks:
        assert chunk.metadata["source"] == "sample.pdf"
        assert chunk.metadata["file_type"] == "pdf"


def test_empty_documents():

    chunks = split_documents([])

    assert chunks == []


def test_chunk_start_index(sample_text):

    document = Document(
        page_content=sample_text,
        metadata={"source": "sample.docx"}
    )

    chunks = split_documents([document])

    assert "start_index" in chunks[0].metadata
    assert chunks[0].metadata["start_index"] == 0