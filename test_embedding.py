from app.services.embedding_service import EmbeddingService


service = EmbeddingService()

chunks = [
    "Python is a popular programming language.",
    "Machine learning allows computers to learn from data.",
    "Deep learning uses neural networks.",
]

embeddings = service.generate_embeddings(chunks)

print("Number of chunks:", len(chunks))
print("Number of embeddings:", len(embeddings))
print("Vector dimension:", len(embeddings[0]))
print("First vector:", embeddings[0][:10])