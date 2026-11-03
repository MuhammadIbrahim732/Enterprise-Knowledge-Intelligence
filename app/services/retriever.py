
from typing import Any

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from app.services.vector_store import get_vector_store


def get_similarity_retriever(
    k: int = 4,
    metadata_filter: dict[str, Any] | None = None
) -> BaseRetriever:

    if k < 1:
        raise ValueError("k must be at least 1.")

    vector_store = get_vector_store()

    search_kwargs = {"k": k}

    if metadata_filter:
        search_kwargs["filter"] = metadata_filter

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs=search_kwargs
    )

    return retriever


def get_mmr_retriever(
    k: int = 4,
    fetch_k: int = 10,
    lambda_mult: float = 0.5,
    metadata_filter: dict[str, Any] | None = None
) -> BaseRetriever:

    if k < 1:
        raise ValueError("k must be at least 1.")

    if fetch_k < k:
        raise ValueError("fetch_k must be greater than or equal to k.")

    if not 0 <= lambda_mult <= 1:
        raise ValueError("lambda_mult must be between 0 and 1.")

    vector_store = get_vector_store()

    search_kwargs = {
        "k": k,
        "fetch_k": fetch_k,
        "lambda_mult": lambda_mult
    }

    if metadata_filter:
        search_kwargs["filter"] = metadata_filter

    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs=search_kwargs
    )

    return retriever


def get_filtered_retriever(
    source: str,
    k: int = 4
) -> BaseRetriever:

    if not source.strip():
        raise ValueError("Source cannot be empty.")

    return get_similarity_retriever(
        k=k,
        metadata_filter={
            "source": source
        }
    )


def get_threshold_retriever(
    k: int = 4,
    score_threshold: float = 0.5,
    metadata_filter: dict[str, Any] | None = None
) -> BaseRetriever:

    if k < 1:
        raise ValueError("k must be at least 1.")

    if not 0 <= score_threshold <= 1:
        raise ValueError("Threshold must be between 0 and 1.")

    vector_store = get_vector_store()

    search_kwargs = {
        "k": k,
        "score_threshold": score_threshold
    }

    if metadata_filter:
        search_kwargs["filter"] = metadata_filter

    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs=search_kwargs
    )

    return retriever

