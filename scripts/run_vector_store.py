
from app.services.document_loader import load_document
from app.services.text_splitter import split_documents

from app.services.vector_store import (
    add_documents,
    search_documents,
    delete_documents
)


# Step 1: Load sample document
documents = load_document("data/uploads/sample.docx")

print("Documents loaded:", len(documents))


# Step 2: Split into chunks
chunks = split_documents(documents)

print("Chunks generated:", len(chunks))


# Step 3: Store chunks in ChromaDB
ids = add_documents(chunks)

print("\nDocuments stored successfully!")

print("Stored IDs:", ids)


try:

    # Step 4: Search using a natural language query
    query = "What is Retrieval Augmented Generation?"

    results = search_documents(
        query=query,
        k=3
    )

    print("\nSemantic Search Results:")

    for index, result in enumerate(results, start=1):

        print(f"\nResult {index}")

        print("Content:", result.page_content)

        print("Metadata:", result.metadata)


    # Step 5: Validate results
    assert len(ids) == len(chunks)
    assert len(results) > 0

    assert results[0].metadata["source"] == "sample.docx"

    print("\nSUCCESS: ChromaDB is working!")


finally:

    # Step 6: Clean up test records
    delete_documents(ids)

    print("\nTest documents deleted successfully!")
