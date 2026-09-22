from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """Service responsible for generating text embeddings."""

    def __init__(self) -> None:
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    def generate_embedding(self, text: str) -> list[float]:
        """Generate an embedding vector for a single text."""
        embedding = self.model.encode(text)

        return embedding.tolist()

    def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        """Generate embedding vectors for multiple texts."""
        embeddings = self.model.encode(texts)

        return embeddings.tolist()