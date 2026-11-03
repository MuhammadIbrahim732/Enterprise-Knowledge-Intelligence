from app.services.document_loader import load_document
from app.services.text_splitter import split_documents
from app.services.vector_store import add_documents, delete_documents
from app.services.rag_service import answer_question


documents = load_document("data/uploads/sample.docx")

chunks = split_documents(documents)

ids = add_documents(chunks)

try:

    question = "Who won the FIFA World Cup in 2018?"

    result = answer_question(question)

    print("\nQUESTION:")
    print(result["question"])

    print("\nANSWER:")
    print(result["answer"])

    print("\nSOURCES:")

    for source in result["sources"]:

        print("\nSource:", source["source"])
        print("File Type:", source["file_type"])
        print("Page:", source["page"])
        print("Content:", source["content"][:200])

finally:

    delete_documents(ids)