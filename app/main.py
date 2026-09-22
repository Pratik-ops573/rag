from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.documents import router as documents_router
from app.core.config import settings
from app.models.database import Base, engine
from app.models.document import Document

from app.api.booking import router as booking_router
from app.models.booking import Booking

# Create database tables.
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)


# Register API routers.
app.include_router(documents_router)
app.include_router(chat_router)
app.include_router(booking_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Palm Mind RAG Backend"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}