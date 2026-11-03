from app.services.llm_service import get_llm


llm = get_llm()

response = llm.invoke("Explain RAG in two simple sentences.")

print("\nGemini Response:")
print(response.content)