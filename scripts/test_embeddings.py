from app.services.embedding_service import (
    embed_documents,
    embed_query
)


# Sample document chunks
texts = [
    "Machine learning is a subset of artificial intelligence.",
    "Deep learning uses neural networks with multiple layers.",
    "Python is a popular programming language."
]


# Generate document embeddings
document_vectors = embed_documents(texts)

print("Document embeddings generated!")

print("Number of documents:", len(document_vectors))

print("Embedding dimensions:", len(document_vectors[0]))


# Generate query embedding
query = "What is deep learning?"

query_vector = embed_query(query)

print("\nQuery embedding generated!")

print("Query dimensions:", len(query_vector))


# Validation
assert len(document_vectors) == 3
assert len(document_vectors[0]) == 768
assert len(query_vector) == 768

print("\nSUCCESS: Gemini embeddings are working!")