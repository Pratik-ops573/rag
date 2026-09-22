from app.models.booking import Booking
from app.models.database import SessionLocal
from app.services.memory_service import MemoryService


session_id = "booking-final-001"

db = SessionLocal()

try:
    booking = (
        db.query(Booking)
        .filter(Booking.id == 4)
        .first()
    )

    print("DATABASE BOOKING:")
    if booking:
        print("ID:", booking.id)
        print("Name:", booking.name)
        print("Email:", booking.email)
        print("Date:", booking.booking_date)
        print("Time:", booking.booking_time)
    else:
        print("Booking not found.")

finally:
    db.close()


memory = MemoryService()

pending_booking = memory.get_booking_data(session_id)

print("\nREDIS PENDING BOOKING:")
print(pending_booking)