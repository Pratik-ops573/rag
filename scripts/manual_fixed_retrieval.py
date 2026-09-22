from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService

document_id = "e815becb-e781-4585-b0ba-518589439ad8"

embedding_service = EmbeddingService()
vector_service = VectorService()

question = "What library is used for data manipulation?"

query_vector = embedding_service.generate_embedding(question)

results = vector_service.search_similar_chunks(
    query_vector=query_vector,
    limit=3,
    document_id=document_id,
)

print("Retrieved chunks:")

for result in results:
    print("\n---")
    print("Score:", result["score"])
    print("Chunk index:", result["chunk_index"])
    print("Text:", result["text"])