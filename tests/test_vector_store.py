from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

import app.services.vector_store as vector_store_service


class FakeEmbeddings(Embeddings):

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [
            [float(len(text)), float(text.count("RAG")), 1.0]
            for text in texts
        ]

    def embed_query(self, text: str) -> list[float]:
        return [
            float(len(text)),
            float(text.count("RAG")),
            1.0
        ]


def setup_vector_store(monkeypatch, tmp_path):

    monkeypatch.setattr(
        vector_store_service.settings,
        "CHROMA_DIR",
        str(tmp_path / "chroma_db")
    )

    monkeypatch.setattr(
        vector_store_service,
        "GeminiEmbeddingAdapter",
        FakeEmbeddings
    )


def test_add_documents(monkeypatch, tmp_path):

    setup_vector_store(monkeypatch, tmp_path)

    documents = [
        Document(
            page_content="RAG combines retrieval and generation.",
            metadata={"source": "sample.pdf"}
        )
    ]

    ids = vector_store_service.add_documents(documents)

    assert len(ids) == 1


def test_search_documents(monkeypatch, tmp_path):

    setup_vector_store(monkeypatch, tmp_path)

    documents = [
        Document(
            page_content="RAG is a retrieval augmented generation system.",
            metadata={"source": "sample.pdf"}
        )
    ]

    ids = vector_store_service.add_documents(documents)

    results = vector_store_service.search_documents(
        query="What is RAG?",
        k=1
    )

    assert len(results) == 1
    assert results[0].metadata["source"] == "sample.pdf"

    vector_store_service.delete_documents(ids)


def test_delete_documents(monkeypatch, tmp_path):

    setup_vector_store(monkeypatch, tmp_path)

    documents = [
        Document(
            page_content="Sample document content.",
            metadata={"source": "sample.pdf"}
        )
    ]

    ids = vector_store_service.add_documents(documents)

    vector_store_service.delete_documents(ids)

    results = vector_store_service.search_documents(
        query="Sample document",
        k=1
    )

    assert results == []


def test_delete_documents_by_source(monkeypatch, tmp_path):

    setup_vector_store(monkeypatch, tmp_path)

    documents = [
        Document(
            page_content="First document chunk.",
            metadata={"source": "guide.pdf"}
        ),
        Document(
            page_content="Second document chunk.",
            metadata={"source": "guide.pdf"}
        )
    ]

    vector_store_service.add_documents(documents)

    deleted_count = vector_store_service.delete_documents_by_source(
        "guide.pdf"
    )

    assert deleted_count == 2


def test_empty_documents(monkeypatch, tmp_path):

    setup_vector_store(monkeypatch, tmp_path)

    import pytest

    with pytest.raises(ValueError):
        vector_store_service.add_documents([])


def test_empty_query():

    import pytest

    with pytest.raises(ValueError):
        vector_store_service.search_documents("")


def test_invalid_k():

    import pytest

    with pytest.raises(ValueError):
        vector_store_service.search_documents(
            query="What is RAG?",
            k=0
        )