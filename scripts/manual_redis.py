from app.services.memory_service import MemoryService


memory_service = MemoryService()

connected = memory_service.test_connection()

print("Redis connected:", connected)