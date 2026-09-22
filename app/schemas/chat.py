from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request body for the conversational RAG API."""

    session_id: str = Field(
        min_length=1,
        description="Unique identifier for the conversation.",
    )

    document_id: str = Field(
        min_length=1,
        description="ID of the uploaded document.",
    )

    question: str = Field(
        min_length=1,
        description="User's question.",
    )


class ChatResponse(BaseModel):
    """Response returned by the conversational RAG API."""

    session_id: str
    document_id: str
    question: str
    answer: str