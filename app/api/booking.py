from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.booking import BookingData, BookingResponse
from app.services.booking_service import BookingService


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)

booking_service = BookingService()


@router.post(
    "",
    response_model=BookingResponse,
)
def create_booking(
    booking_data: BookingData,
    db: Annotated[Session, Depends(get_db)],
) -> BookingResponse:
    """Create an interview booking."""

    booking = booking_service.create_booking(
        db=db,
        booking_data=booking_data,
    )

    return BookingResponse(
        id=booking.id,
        name=booking.name,
        email=booking.email,
        booking_date=booking.booking_date,
        booking_time=booking.booking_time,
    )