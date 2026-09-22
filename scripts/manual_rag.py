from app.services.rag_service import RAGService


rag_service = RAGService()

document_id = "acfc9080-5eec-4fee-bb27-6d99dd62a03f"
session_id = "test-rag-session-001"

question = "can u tell me more about it?"

answer = rag_service.generate_answer(
    question=question,
    document_id=document_id,
    session_id=session_id,
    top_k=3,
)

print("\nRAG Answer:")
print(answer)