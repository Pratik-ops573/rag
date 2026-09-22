from sqlalchemy.orm import Session

from app.schemas.booking import BookingData, BookingExtraction
from app.services.booking_service import BookingService
from app.services.memory_service import MemoryService
from app.services.rag_service import RAGService


class ConversationService:
    """Service responsible for handling conversational requests."""

    def __init__(self) -> None:
        """Initialize conversation dependencies."""

        self.booking_service = BookingService()
        self.memory_service = MemoryService()
        self.rag_service = RAGService()

    def handle_message(
        self,
        question: str,
        document_id: str,
        session_id: str,
        db: Session,
    ) -> tuple[str, BookingData | None]:
        """
        Handle a conversational message.

        Supports normal RAG questions and multi-turn
        interview booking.
        """

        # Check whether this session already has
        # an incomplete booking.
        existing_booking = self.memory_service.get_booking_data(
            session_id
        )

        # Only call the booking LLM when:
        # 1. A booking is already in progress, or
        # 2. The new message appears to be about interview booking.
        booking_extraction = None

        if (
            existing_booking is not None
            or self._looks_like_booking_request(question)
        ):
            booking_extraction = (
                self.booking_service.extract_booking_data(
                    message=question,
                    booking_in_progress=existing_booking is not None,
                )
            )

            # If a booking is already in progress, merge
            # previous information with the new information.
            if existing_booking is not None:
                booking_extraction = self._merge_booking_data(
                    existing_booking,
                    booking_extraction,
                )

        # Handle booking flow.
        if (
            booking_extraction is not None
            and booking_extraction.is_booking
        ):
            missing_fields = self._get_missing_fields(
                booking_extraction
            )

            # Booking is incomplete.
            if missing_fields:
                booking_data = booking_extraction.model_dump(
                    mode="json"
                )

                self.memory_service.save_booking_data(
                    session_id=session_id,
                    booking_data=booking_data,
                )

                answer = self._build_missing_fields_response(
                    booking_extraction,
                    missing_fields,
                )

                self.memory_service.save_message(
                    session_id=session_id,
                    role="user",
                    content=question,
                )

                self.memory_service.save_message(
                    session_id=session_id,
                    role="assistant",
                    content=answer,
                )

                return answer, None

            # Booking is complete.
            booking_data = BookingData(
                name=booking_extraction.name,
                email=booking_extraction.email,
                booking_date=booking_extraction.booking_date,
                booking_time=booking_extraction.booking_time,
            )

            booking = self.booking_service.create_booking(
                db=db,
                booking_data=booking_data,
            )

            # Clear pending booking because it is complete.
            self.memory_service.clear_booking_data(
                session_id
            )

            answer = (
                "Your interview has been booked successfully. "
                f"Booking ID: {booking.id}. "
                f"Date: {booking.booking_date}. "
                f"Time: {booking.booking_time}."
            )

            self.memory_service.save_message(
                session_id=session_id,
                role="user",
                content=question,
            )

            self.memory_service.save_message(
                session_id=session_id,
                role="assistant",
                content=answer,
            )

            return answer, booking_data

        # Normal RAG question.
        answer = self.rag_service.generate_answer(
            question=question,
            document_id=document_id,
            session_id=session_id,
        )

        return answer, None

    @staticmethod
    def _looks_like_booking_request(message: str) -> bool:
        """Detect whether a message is likely related to interview booking."""

        booking_keywords = {
            "book",
            "booking",
            "schedule",
            "scheduled",
            "appointment",
            "interview",
            "meeting",
            "reschedule",
        }

        message_words = set(
            message.lower()
            .replace(".", " ")
            .replace(",", " ")
            .replace("?", " ")
            .replace("!", " ")
            .split()
        )

        return bool(message_words & booking_keywords)

    @staticmethod
    def _merge_booking_data(
        existing: dict,
        current: BookingExtraction,
    ) -> BookingExtraction:
        """Merge previous booking information with new information."""

        return BookingExtraction(
            is_booking=True,
            name=current.name or existing.get("name"),
            email=current.email or existing.get("email"),
            booking_date=(
                current.booking_date
                or existing.get("booking_date")
            ),
            booking_time=(
                current.booking_time
                or existing.get("booking_time")
            ),
        )

    @staticmethod
    def _get_missing_fields(
        booking: BookingExtraction,
    ) -> list[str]:
        """Return booking fields that are still missing."""

        missing_fields: list[str] = []

        if booking.name is None:
            missing_fields.append("name")

        if booking.email is None:
            missing_fields.append("email")

        if booking.booking_date is None:
            missing_fields.append("date")

        if booking.booking_time is None:
            missing_fields.append("time")

        return missing_fields

    @staticmethod
    def _build_missing_fields_response(
        booking: BookingExtraction,
        missing_fields: list[str],
    ) -> str:
        """Build a response requesting missing booking information."""

        if booking.name:
            greeting = f"Thanks, {booking.name}."
        else:
            greeting = "Sure."

        if len(missing_fields) == 1:
            fields_text = missing_fields[0]

        elif len(missing_fields) == 2:
            fields_text = (
                f"{missing_fields[0]} and "
                f"{missing_fields[1]}"
            )

        else:
            fields_text = (
                ", ".join(missing_fields[:-1])
                + f", and {missing_fields[-1]}"
            )

        return (
            f"{greeting} "
            f"Please provide your {fields_text} "
            "so I can complete the interview booking."
        )