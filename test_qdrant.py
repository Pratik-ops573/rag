from app.services.vector_service import VectorService


service = VectorService()

print("Qdrant connected:", service.test_connection())

service.create_collection()

print("Collection created:", service.COLLECTION_NAME)