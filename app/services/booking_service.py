from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.schemas.booking import BookingData
from app.services.llm_service import LLMService


class BookingService:
    """Service responsible for interview booking operations."""

    def __init__(self) -> None:
        """Initialize the booking service."""

        self.llm_service = LLMService()

    def extract_booking_data(
        self,
        message: str,
    ) -> BookingData | None:
        """
        Extract and validate booking information from
        a natural-language message.
        """

        extracted_data = self.llm_service.extract_booking_data(
            message
        )

        if not extracted_data.get("is_booking"):
            return None

        required_fields = (
            "name",
            "email",
            "booking_date",
            "booking_time",
        )

        if any(
            extracted_data.get(field) is None
            for field in required_fields
        ):
            return None

        return BookingData(
            name=extracted_data["name"],
            email=extracted_data["email"],
            booking_date=extracted_data["booking_date"],
            booking_time=extracted_data["booking_time"],
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