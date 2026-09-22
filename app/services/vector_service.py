from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.core.config import settings


class VectorService:
    """Service responsible for interacting with Qdrant."""

    COLLECTION_NAME = "palm_mind_documents"
    VECTOR_SIZE = 384

    def __init__(self) -> None:
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )

    def test_connection(self) -> bool:
        """Check whether the application can connect to Qdrant."""
        self.client.get_collections()
        return True

    def create_collection(self) -> None:
        """Create the document vector collection if it does not exist."""
        collections = self.client.get_collections()

        existing_names = {
            collection.name for collection in collections.collections
        }

        if self.COLLECTION_NAME not in existing_names:
            self.client.create_collection(
                collection_name=self.COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=self.VECTOR_SIZE,
                    distance=Distance.COSINE,
                ),
            )