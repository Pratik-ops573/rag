from app.services.booking_service import BookingService


booking_service = BookingService()


message = """
Hi, I would like to book an interview.
My name is John Doe.
My email is john@example.com.
I am available on September 25, 2026 at 2 PM.
"""


booking_data = booking_service.extract_booking_data(message)


print("\nValidated booking data:")

if booking_data:
    print(booking_data.model_dump())
else:
    print("No booking detected.")