from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.core.config import settings

from typing import Any


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

    def insert_chunk(
        self,
        vector: list[float],
        document_id: str,
        chunk_index: int,
        text: str,
    ) -> str:
        """Store one embedded document chunk in Qdrant."""
        point_id = str(uuid4())

        point = PointStruct(
            id=point_id,
            vector=vector,
            payload={
                "document_id": document_id,
                "chunk_index": chunk_index,
                "text": text,
            },
        )

        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[point],
        )

        return point_id

    def search_similar_chunks(
        self,
        query_vector: list[float],
        limit: int = 3,
    ) -> list[dict[str, Any]]:
        """Search Qdrant for chunks similar to the query vector."""
        response = self.client.query_points(
            collection_name=self.COLLECTION_NAME,
            query=query_vector,
            limit=limit,
            with_payload=True,
        )

        results: list[dict[str, Any]] = []

        for point in response.points:
            payload = point.payload or {}

            results.append(
                {
                    "score": point.score,
                    "document_id": payload.get("document_id"),
                    "chunk_index": payload.get("chunk_index"),
                    "text": payload.get("text"),
                }
            )

        return results

    def insert_chunks(
        self,
        vectors: list[list[float]],
        document_id: str,
        chunks: list[str],
    ) -> int:
        """Store multiple embedded chunks in Qdrant."""
        if len(vectors) != len(chunks):
            raise ValueError("vectors and chunks must have the same length.")

        points: list[PointStruct] = []

        for index, (vector, chunk) in enumerate(zip(vectors, chunks)):
            points.append(
                PointStruct(
                    id=str(uuid4()),
                    vector=vector,
                    payload={
                        "document_id": document_id,
                        "chunk_index": index,
                        "text": chunk,
                    },
                )
            )

        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=points,
        )

        return len(points)