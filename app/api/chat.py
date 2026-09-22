from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.conversation_service import ConversationService


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

conversation_service = ConversationService()


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    db: Annotated[Session, Depends(get_db)],
) -> ChatResponse:
    """Handle conversational RAG and interview booking."""

    answer, _ = conversation_service.handle_message(
        question=request.question,
        document_id=request.document_id,
        session_id=request.session_id,
        db=db,
    )

    return ChatResponse(
        session_id=request.session_id,
        document_id=request.document_id,
        question=request.question,
        answer=answer,
    )