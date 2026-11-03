from app.services.document_loader import load_document
from app.services.text_splitter import split_documents
from app.services.vector_store import add_documents, delete_documents

from app.services.retriever import (
    get_similarity_retriever,
    get_mmr_retriever,
    get_filtered_retriever,
    get_threshold_retriever
)


# Load and store sample document
documents = load_document("data/uploads/sample.docx")
chunks = split_documents(documents)

ids = add_documents(chunks)

try:

    query = "What is Retrieval Augmented Generation?"

    # 1. Similarity Search
    print("\n1. SIMILARITY SEARCH")

    similarity = get_similarity_retriever(k=3)
    results = similarity.invoke(query)

    print("Results:", len(results))

    for result in results:
        print(result.page_content[:200])

    assert len(results) > 0


    # 2. MMR Search
    print("\n2. MMR SEARCH")

    mmr = get_mmr_retriever(
        k=2,
        fetch_k=5,
        lambda_mult=0.5
    )

    results = mmr.invoke(query)

    print("Results:", len(results))

    assert len(results) > 0


    # 3. Metadata Filtering
    print("\n3. METADATA FILTERING")

    filtered = get_filtered_retriever(
        source="sample.docx",
        k=3
    )

    results = filtered.invoke(query)

    print("Results:", len(results))

    assert len(results) > 0

    assert all(
        result.metadata["source"] == "sample.docx"
        for result in results
    )


    # 4. Top-K Retrieval
    print("\n4. TOP-K RETRIEVAL")

    top_k = get_similarity_retriever(k=2)

    results = top_k.invoke(query)

    print("Results:", len(results))

    assert len(results) <= 2


    # 5. Score Threshold
    print("\n5. SCORE THRESHOLD")

    threshold = get_threshold_retriever(
        k=3,
        score_threshold=0.0
    )

    results = threshold.invoke(query)

    print("Results:", len(results))

    assert len(results) > 0


    print("\nSUCCESS: All retriever tests passed!")


finally:

    delete_documents(ids)

    print("\nTest documents deleted.")
