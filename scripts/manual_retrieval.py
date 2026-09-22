from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService

document_id = "acfc9080-5eec-4fee-bb27-6d99dd62a03f"

embedding_service = EmbeddingService()
vector_service = VectorService()

question = "What programming language is mentioned in the document?"

query_vector = embedding_service.generate_embedding(question)

results = vector_service.search_similar_chunks(
    query_vector=query_vector,
    limit=3,
    document_id=document_id,
)

for result in results:
    print("\n--- RESULT ---")
    print("Score:", result["score"])
    print("Chunk index:", result["chunk_index"])
    print("Text:")
    print(result["text"])