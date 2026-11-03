from langchain.embeddings import Embeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.core.config import settings

def get_embedding_model():
    embeddings = GoogleGenerativeAIEmbeddings(
        model = settings.EMBEDDING_MODEL,
        google_api_key = settings.GEMINI_API_KEY,
        task_type = "RETRIEVAL_DOCUMENT",
        output_dimensionality = settings.EMBEDDING_DIMENSION
    )
    return embeddings


def embed_documents(texts:list[str]) -> list[list[float]]:
    embeddings = get_embedding_model()
    vectors = embeddings.embed_documents(texts)
    return vectors


def embed_query(query: str) -> list[float]:
     embeddings = GoogleGenerativeAIEmbeddings(
        model = settings.EMBEDDING_MODEL,
        google_api_key = settings.GEMINI_API_KEY,
        task_type = "RETRIEVAL_QUERY",
        output_dimensionality = settings.EMBEDDING_DIMENSION
    )
     
     vector = embeddings.embed_query(query)
     return vector


class GeminiEmbeddingAdapter(Embeddings):

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return embed_documents(texts)

    def embed_query(self, texts: str) -> list[float]:
            return embed_query(texts)

