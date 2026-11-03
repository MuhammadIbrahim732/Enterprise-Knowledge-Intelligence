from fastapi import APIRouter, HTTPException

from app.schemas.api_schemas import ChatRequest, ChatResponse
from app.services.rag_service import answer_question


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):

    try:

        result = answer_question(
            question=request.question,
            k=request.k
        )

        return ChatResponse(
            question=result["question"],
            answer=result["answer"],
            sources=result["sources"]
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Chat processing failed: {str(error)}"
        )