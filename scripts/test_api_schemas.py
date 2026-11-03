from app.schemas.api_schemas import (
    ChatRequest,
    ChatResponse,
    SourceCitation,
    UploadResponse,
    HealthResponse
)


# Test Chat Request
chat_request = ChatRequest(
    question="What is RAG?",
    k=4
)

print("Chat Request:")
print(chat_request.model_dump())


# Test Source Citation
source = SourceCitation(
    source="rag_guide.pdf",
    file_type="pdf",
    page=3,
    content="RAG combines retrieval and generation."
)

print("\nSource Citation:")
print(source.model_dump())


# Test Chat Response
chat_response = ChatResponse(
    question="What is RAG?",
    answer="RAG combines retrieval with generation.",
    sources=[source]
)

print("\nChat Response:")
print(chat_response.model_dump())


# Test Upload Response
upload_response = UploadResponse(
    filename="rag_guide.pdf",
    message="Document uploaded successfully.",
    chunks_created=10
)

print("\nUpload Response:")
print(upload_response.model_dump())


# Test Health Response
health_response = HealthResponse(
    status="healthy",
    application="Enterprise Knowledge Intelligence"
)

print("\nHealth Response:")
print(health_response.model_dump())