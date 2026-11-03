from unittest.mock import MagicMock

import pytest
from langchain_core.documents import Document

import app.services.rag_service as rag_service


@pytest.fixture
def sample_documents():

    return [
        Document(
            page_content="RAG combines information retrieval with language generation.",
            metadata={
                "source": "rag_guide.pdf",
                "file_type": "pdf",
                "page": 2
            }
        )
    ]


def test_format_documents(sample_documents):

    context = rag_service.format_documents(sample_documents)

    assert "RAG combines" in context


def test_format_sources(sample_documents):

    sources = rag_service.format_sources(sample_documents)

    assert len(sources) == 1
    assert sources[0]["source"] == "rag_guide.pdf"
    assert sources[0]["page"] == 3


def test_answer_question(monkeypatch, sample_documents):

    mock_retriever = MagicMock()
    mock_retriever.invoke.return_value = sample_documents

    monkeypatch.setattr(
        rag_service,
        "get_similarity_retriever",
        lambda k: mock_retriever
    )

    mock_llm = MagicMock()

    monkeypatch.setattr(
        rag_service,
        "get_llm",
        lambda: mock_llm
    )

    mock_chain = MagicMock()

    mock_chain.invoke.return_value = (
    "RAG combines retrieval and generation."
)

    monkeypatch.setattr(
       rag_service,
       "create_rag_chain",
       lambda: mock_chain
)

    result = rag_service.answer_question(
        question="What is RAG?",
        k=4
    )

    assert result["question"] == "What is RAG?"
    assert result["answer"] == "RAG combines retrieval and generation."
    assert len(result["sources"]) == 1


def test_empty_question():

    with pytest.raises(ValueError):

        rag_service.answer_question("")


def test_no_retrieved_documents(monkeypatch):

    mock_retriever = MagicMock()
    mock_retriever.invoke.return_value = []

    monkeypatch.setattr(
        rag_service,
        "get_similarity_retriever",
        lambda k: mock_retriever
    )

    result = rag_service.answer_question(
        question="What is RAG?"
    )

    assert result["sources"] == []
    assert "couldn't find" in result["answer"]