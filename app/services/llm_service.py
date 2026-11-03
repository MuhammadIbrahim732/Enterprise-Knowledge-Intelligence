from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings


def get_llm() -> ChatGoogleGenerativeAI:

    llm = ChatGoogleGenerativeAI(
        model=settings.LLM_MODEL,
        google_api_key=settings.GEMINI_API_KEY,
        temperature=0.2,
        max_retries=2
    )

    return llm