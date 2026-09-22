import json
from typing import Any

import redis

from app.core.config import settings


class MemoryService:
    """Service responsible for Redis-based chat memory."""

    def __init__(self) -> None:
        """Initialize the Redis client."""

        self.client = redis.from_url(
            settings.redis_url,
            decode_responses=True,
        )

    def test_connection(self) -> bool:
        """Check whether the application can connect to Redis."""

        return bool(self.client.ping())

    def save_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ) -> None:
        """Save a single chat message to Redis."""

        key = f"chat:{session_id}"

        message = {
            "role": role,
            "content": content,
        }

        self.client.rpush(
            key,
            json.dumps(message),
        )

    def get_history(
        self,
        session_id: str,
    ) -> list[dict[str, str]]:
        """Retrieve the complete chat history for a session."""

        key = f"chat:{session_id}"

        messages = self.client.lrange(
            key,
            0,
            -1,
        )

        return [
            json.loads(message)
            for message in messages
        ]

    def clear_history(
        self,
        session_id: str,
    ) -> None:
        """Delete chat history for a session."""

        key = f"chat:{session_id}"

        self.client.delete(key)

    def save_booking_data(
        self,
        session_id: str,
        booking_data: dict[str, Any],
    ) -> None:
        """Save incomplete booking information to Redis."""

        key = f"booking:{session_id}"

        self.client.set(
            key,
            json.dumps(booking_data),
        )

    def get_booking_data(
        self,
        session_id: str,
    ) -> dict[str, Any] | None:
        """Retrieve pending booking information from Redis."""

        key = f"booking:{session_id}"

        data = self.client.get(key)

        if data is None:
            return None

        return json.loads(data)

    def clear_booking_data(
        self,
        session_id: str,
    ) -> None:
        """Delete pending booking information from Redis."""

        key = f"booking:{session_id}"

        self.client.delete(key)