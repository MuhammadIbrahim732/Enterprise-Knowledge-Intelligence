from app.services.document_loader import load_document
from app.services.text_splitter import split_documents
from app.services.vector_store import add_documents, delete_documents
from app.services.rag_service import answer_question


# 1. Load document
documents = load_document("data/uploads/sample.docx")

# 2. Split into chunks
chunks = split_documents(documents)

# 3. Store chunks in ChromaDB
ids = add_documents(chunks)

try:
    # 4. Ask a question
    question = "What is the main topic of this document?"

    result = answer_question(question)

    print("\nQuestion:")
    print(result["question"])

    print("\nAnswer:")
    print(result["answer"])

    print("\nRetrieved Sources:")

    for document in result["sources"]:
        print(document.metadata)

finally:
    # 5. Clean up test records
    delete_documents(ids)