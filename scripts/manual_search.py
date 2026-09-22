from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService


embedding_service = EmbeddingService()
vector_service = VectorService()

query = "What programming language is popular?"

query_vector = embedding_service.generate_embedding(query)

results = vector_service.search_similar_chunks(
    query_vector=query_vector,
    limit=3,
)

print("\nSearch results:")

for result in results:
    print("\nScore:", result["score"])
    print("Document ID:", result["document_id"])
    print("Chunk index:", result["chunk_index"])
    print("Text:", result["text"])