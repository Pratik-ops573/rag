from fastapi import FastAPI

from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Palm Mind RAG Backend"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}