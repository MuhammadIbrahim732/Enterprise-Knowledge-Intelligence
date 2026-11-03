from pydantic import BaseModel, Field, field_validator

# Chat Request
class ChatRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=2000,
        description="Question asked by the user"
    )

    k: int = Field(
        default=4,
        ge=1,
        le=10,
        description="Number of document chunks to retrieve"
    )

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Question cannot be empty.")

        return value

# Source Citation
class SourceCitation(BaseModel):

    source: str

    file_type: str

    page: int | None = None

    content: str


# Chat Response
class ChatResponse(BaseModel):

    question: str

    answer: str

    sources: list[SourceCitation]


# Upload Response
class UploadResponse(BaseModel):

    filename: str

    message: str

    chunks_created: int


# Health Response
class HealthResponse(BaseModel):

    status: str

    application: str