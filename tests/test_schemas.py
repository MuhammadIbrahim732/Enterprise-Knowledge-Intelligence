from app.schemas.api_schemas import (
    ChatRequest,
    SourceCitation,
    UploadResponse,
    HealthResponse
)


def test_chat_request():

    request = ChatRequest(
        question="What is RAG?",
        k=4
    )

    assert request.question == "What is RAG?"
    assert request.k == 4


def test_chat_request_default_k():

    request = ChatRequest(
        question="Explain embeddings."
    )

    assert request.k == 4


def test_source_citation():

    source = SourceCitation(
        source="guide.pdf",
        file_type="pdf",
        page=2,
        content="Sample content"
    )

    assert source.source == "guide.pdf"
    assert source.page == 2


def test_upload_response():

    response = UploadResponse(
        filename="guide.pdf",
        message="Uploaded successfully.",
        chunks_created=5
    )

    assert response.chunks_created == 5


def test_health_response():

    response = HealthResponse(
        status="healthy",
        application="Enterprise Knowledge Intelligence"
    )

    assert response.status == "healthy"