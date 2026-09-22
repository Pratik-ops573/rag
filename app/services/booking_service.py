from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.schemas.booking import BookingData, BookingExtraction
from app.services.llm_service import LLMService


class BookingService:
    """Service responsible for interview booking operations."""

    def __init__(self) -> None:
        """Initialize the booking service."""

        self.llm_service = LLMService()

    def extract_booking_data(
        self,
        message: str,
        booking_in_progress: bool = False,
    ) -> BookingExtraction:
        """
        Extract booking information from a natural-language message.

        The result may contain partial booking information.
        """

        extracted_data = self.llm_service.extract_booking_data(
            message=message,
            booking_in_progress=booking_in_progress,
        )

        return BookingExtraction(
            **extracted_data
        )

    def create_booking(
        self,
        db: Session,
        booking_data: BookingData,
    ) -> Booking:
        """Create and store a new interview booking."""

        booking = Booking(
            name=booking_data.name,
            email=booking_data.email,
            booking_date=booking_data.booking_date,
            booking_time=booking_data.booking_time,
        )

        db.add(booking)
        db.commit()
        db.refresh(booking)

        return booking