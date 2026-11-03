from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def split_documents(documents: list[Document]) -> list[Document]:

    # Remove leading and trailing whitespace
    cleaned_documents = []

    for document in documents:
        cleaned_document = Document(
            page_content=document.page_content.strip(),
            metadata=document.metadata.copy()
        )

        cleaned_documents.append(cleaned_document)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = splitter.split_documents(cleaned_documents)

    return chunks