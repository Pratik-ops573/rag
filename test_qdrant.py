from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService


embedding_service = EmbeddingService()
vector_service = VectorService()

vector_service.create_collection()

text = "Python is a popular programming language."

vector = embedding_service.generate_embedding(text)

point_id = vector_service.insert_chunk(
    vector=vector,
    document_id="test-document-001",
    chunk_index=0,
    text=text,
)

print("Inserted point:", point_id)