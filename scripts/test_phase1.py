
from pathlib import Path

from docx import Document as DocxDocument

from app.services.document_loader import load_document
from app.services.text_splitter import split_documents


# Create a sample DOCX document
sample_path = Path("data/uploads/sample.docx")

doc = DocxDocument()

doc.add_heading("Enterprise AI Knowledge Management", level=1)

doc.add_paragraph(
    "Retrieval Augmented Generation (RAG) combines "
    "information retrieval with large language models. "
    "It allows applications to retrieve relevant information "
    "from external documents before generating answers."
)

doc.add_paragraph(
    "Vector databases store numerical representations "
    "of text called embeddings. These embeddings allow "
    "semantic similarity searches."
)

doc.save(sample_path)

print("\n1. Sample DOCX created successfully.")


# Load document
documents = load_document(str(sample_path))

print("\n2. Document extraction completed.")

for document in documents:
    print("Content:", document.page_content)
    print("Metadata:", document.metadata)


# Split document
chunks = split_documents(documents)

print("\n3. Chunking completed.")

print("Total documents:", len(documents))
print("Total chunks:", len(chunks))

for index, chunk in enumerate(chunks):

    print(f"\nChunk {index + 1}")
    print("Content:", chunk.page_content)
    print("Metadata:", chunk.metadata)


# Basic assertions
assert len(documents) > 0
assert len(chunks) > 0

assert chunks[0].metadata["source"] == "sample.docx"

assert all(
    len(chunk.page_content) <= 1000
    for chunk in chunks
)

print("\nSUCCESS: Phase 1 document processing works!")
