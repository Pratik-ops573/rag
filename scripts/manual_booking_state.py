from app.services.memory_service import MemoryService

memory = MemoryService()

data = memory.get_booking_data("booking-final-001")

print("Pending booking data:")
print(data)
