from qdrant_client.models import PayloadSchemaType

from app.services.vector_service import VectorService


vector_service = VectorService()

vector_service.client.create_payload_index(
    collection_name=vector_service.COLLECTION_NAME,
    field_name="document_id",
    field_schema=PayloadSchemaType.KEYWORD,
)

print("document_id payload index created.")