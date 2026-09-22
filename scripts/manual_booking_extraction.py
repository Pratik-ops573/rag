from app.services.llm_service import LLMService


llm_service = LLMService()


message = """
Hi, I would like to book an interview.
My name is John Doe.
My email is john@example.com.
I am available on September 25, 2026 at 2 PM.
"""


result = llm_service.extract_booking_data(message)

print("\nBooking extraction:")
print(result)