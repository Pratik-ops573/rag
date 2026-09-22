from datetime import date, time

from pydantic import BaseModel, EmailStr, Field

class BookingExtraction(BaseModel):
    """Partially extracted booking information from a conversation."""

    is_booking: bool

    name: str | None = None
    email: EmailStr | None = None
    booking_date: date | None = None
    booking_time: time | None = None

class BookingData(BaseModel):
    """Validated interview booking information."""

    name: str = Field(
        min_length=1,
        max_length=100,
    )

    email: EmailStr

    booking_date: date

    booking_time: time


class BookingResponse(BaseModel):
    """Response returned after creating a booking."""

    id: int
    name: str
    email: EmailStr
    booking_date: date
    booking_time: time