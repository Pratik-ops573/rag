from sqlalchemy.orm import Session

from app.schemas.booking import BookingData
from app.services.booking_service import BookingService
from app.services.rag_service import RAGService


class ConversationService:
    """Service responsible for handling conversational requests."""

    def __init__(self) -> None:
        """Initialize conversation dependencies."""

        self.booking_service = BookingService()
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

        Returns the generated answer and optional booking data.
        """

        booking_data = self.booking_service.extract_booking_data(
            question
        )

        if booking_data is not None:
            booking = self.booking_service.create_booking(
                db=db,
                booking_data=booking_data,
            )

            answer = (
                "Your interview has been booked successfully. "
                f"Booking ID: {booking.id}. "
                f"Date: {booking.booking_date}. "
                f"Time: {booking.booking_time}."
            )

            return answer, booking_data

        answer = self.rag_service.generate_answer(
            question=question,
            document_id=document_id,
            session_id=session_id,
        )

        return answer, None