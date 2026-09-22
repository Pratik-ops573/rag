from typing import Any
from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PayloadSchemaType,
    PointStruct,
    VectorParams,
)

from app.core.config import settings


class VectorService:
    """Service responsible for interacting with Qdrant."""

    COLLECTION_NAME = "palm_mind_documents"
    VECTOR_SIZE = 384

    def __init__(self) -> None:
        """Initialize the Qdrant client."""
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )

    def test_connection(self) -> bool:
        """Check whether the application can connect to Qdrant."""
        self.client.get_collections()
        return True

    def create_collection(self) -> None:
        """
        Create the document collection if it does not exist.

        Also creates the document_id payload index required
        for filtered similarity searches.
        """

        collections = self.client.get_collections()

        existing_names = {
            collection.name
            for collection in collections.collections
        }

        if self.COLLECTION_NAME not in existing_names:
            self.client.create_collection(
                collection_name=self.COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=self.VECTOR_SIZE,
                    distance=Distance.COSINE,
                ),
            )

        self.client.create_payload_index(
            collection_name=self.COLLECTION_NAME,
            field_name="document_id",
            field_schema=PayloadSchemaType.KEYWORD,
        )

    def insert_chunk(
        self,
        vector: list[float],
        document_id: str,
        chunk_index: int,
        text: str,
    ) -> str:
        """Store a single embedded document chunk in Qdrant."""

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

    def insert_chunks(
        self,
        vectors: list[list[float]],
        document_id: str,
        chunks: list[str],
    ) -> int:
        """Store multiple embedded document chunks in Qdrant."""

        if len(vectors) != len(chunks):
            raise ValueError(
                "vectors and chunks must have the same length."
            )

        points: list[PointStruct] = []

        for index, (vector, chunk) in enumerate(
            zip(vectors, chunks)
        ):
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

    def search_similar_chunks(
        self,
        query_vector: list[float],
        limit: int = 3,
        document_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Search Qdrant for semantically similar document chunks.

        If document_id is provided, results are restricted to
        chunks belonging to that document.
        """

        query_filter = None

        if document_id is not None:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(value=document_id),
                    )
                ]
            )

        response = self.client.query_points(
            collection_name=self.COLLECTION_NAME,
            query=query_vector,
            query_filter=query_filter,
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