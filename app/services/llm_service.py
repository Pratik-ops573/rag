import json

from openai import OpenAI

from app.core.config import settings


class LLMService:
    """Service responsible for interacting with the OpenRouter LLM."""

    def __init__(self) -> None:
        """Initialize the OpenRouter client."""

        self.client = OpenAI(
            api_key=settings.openrouter_api_key,
            base_url="https://openrouter.ai/api/v1",
        )

    def generate_response(self, prompt: str) -> str:
        """Generate a text response from the OpenRouter LLM."""

        response = self.client.chat.completions.create(
            model=settings.openrouter_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content or ""

    def extract_booking_data(
        self,
        message: str,
        booking_in_progress: bool = False,
    ) -> dict:
        """
        Extract interview booking information from a user message.

        If a booking is already in progress, the message is treated
        as a continuation of that booking.
        """

        if booking_in_progress:
            instruction = """
A booking is already in progress.

The user may be providing one or more missing booking
fields in this message.

Extract any booking information present in the message.

Examples:

"My email is alice@example.com."
-> extract the email

"September 25, 2026 at 2 PM."
-> extract the date and time

"My name is John Doe."
-> extract the name

"Actually, make it 3 PM."
-> extract the new time

Treat this message as part of the existing booking.
"""
        else:
            instruction = """
Determine whether the user's message contains an
interview booking request.

If it is NOT a booking request, return:

{"is_booking": false}

If it IS a booking request, extract the booking fields.
"""

        prompt = f"""
You are an information extraction assistant.

{instruction}

Extract these fields:

- name
- email
- booking_date
- booking_time

Return ONLY valid JSON.

Use exactly this structure:

{{
    "is_booking": true or false,
    "name": "string or null",
    "email": "string or null",
    "booking_date": "YYYY-MM-DD or null",
    "booking_time": "HH:MM or null"
}}

Rules:

- Do not invent missing information.
- Use null when a field is not present.
- Convert dates to YYYY-MM-DD.
- Convert times to 24-hour HH:MM format.
- Do not add markdown.
- Do not add explanations.

User message:
{message}
"""

        response = self.client.chat.completions.create(
            model=settings.openrouter_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        content = response.choices[0].message.content or ""

        return json.loads(content)