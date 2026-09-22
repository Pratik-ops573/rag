import json

from google import genai

from app.core.config import settings


class LLMService:
    """Service responsible for interacting with the Gemini LLM."""

    MODEL_NAME = "gemini-3.6-flash"

    def __init__(self) -> None:
        """Initialize the Gemini client."""

        self.client = genai.Client(
            api_key=settings.gemini_api_key,
        )

    def generate_response(self, prompt: str) -> str:
        """Generate a text response from Gemini."""

        interaction = self.client.interactions.create(
            model=self.MODEL_NAME,
            input=prompt,
        )

        return interaction.output_text or ""

    def extract_booking_data(self, message: str) -> dict:
        """Extract interview booking information from a user message."""

        prompt = f"""
You are an information extraction assistant.

Determine whether the user's message contains an interview booking request.

If it is NOT a booking request, return exactly:

{{"is_booking": false}}

If it IS a booking request, extract these fields:

- name
- email
- booking_date
- booking_time

Return ONLY valid JSON.

Use this exact structure:

{{
    "is_booking": true,
    "name": "string or null",
    "email": "string or null",
    "booking_date": "YYYY-MM-DD or null",
    "booking_time": "HH:MM or null"
}}

Do not add markdown.
Do not add explanations.

User message:
{message}
"""

        interaction = self.client.interactions.create(
            model=self.MODEL_NAME,
            input=prompt,
        )

        response = interaction.output_text or ""

        return json.loads(response)