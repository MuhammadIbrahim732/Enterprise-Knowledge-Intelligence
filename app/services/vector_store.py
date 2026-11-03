import uuid
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.core.config import settings
from app.services.embedding_service import GeminiEmbeddingAdapter

COLLECTION_NAME = "enterprise_knowledge"

def get_vector_store() -> Chroma:

    Path(settings.CHROMA_DIR).mkdir(
        parents = True,
        exist_ok = True
    )


    # Initialize persistent ChromaDB
    vector_Store = Chroma(
        collection_name= COLLECTION_NAME,
        embedding_function = GeminiEmbeddingAdapter(),
        persist_directory = settings.CHROMA_DIR,
        collection_metadata = {
            "hnsw:space" : "cosine"
        }
    )

    return vector_Store

def add_documents(documents: list[Document]) -> list[str]:

    if not documents:
        raise ValueError("No documents provided.")

    vector_Store = get_vector_store()

    # Generate unique IDs
    ids = [
        str(uuid.uuid4())
        for _ in documents
    ]

    # Store documents and their embeddings
    stored_ids = vector_Store.add_documents(
        documents = documents,
        ids = ids
    )

    return stored_ids


def search_documents(
        query: str,
        k: int = 4
    ) -> list[Document]:

    if not query.strip():
        raise ValueError("Query cannot be empty.")

    if k < 1:
        raise ValueError("k must be at least 1.")

    vector_Store = get_vector_store()

    results = vector_Store.similarity_search(
        query = query,
        k = k
    )

    return results

def delete_documents(ids: list[str]) -> None:

    if not ids:
        raise ValueError("No document IDs provided.")

    vector_store = get_vector_store()

    vector_store.delete(ids = ids)

def delete_documents_by_source(source: str) -> int:

    if not source.strip():
        raise ValueError("Source cannot be empty.")

    vector_store = get_vector_store()

    # Find all chunks belonging to this document
    results = vector_store._collection.get(
        where={"source": source}
    )

    ids = results["ids"]

    if ids:
        vector_store.delete(ids=ids)

    return len(ids)