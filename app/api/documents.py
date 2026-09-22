from uuid import uuid4
from typing import Annotated

from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService

from fastapi import APIRouter, File, HTTPException, Query, UploadFile

from app.services.chunking_service import ChunkingStrategy, chunk_text
from app.utils.text_extraction import (
    extract_text_from_pdf,
    extract_text_from_txt,
)
from app.models.database import SessionLocal
from app.models.document import Document

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post("/upload")
async def upload_document(
    file: Annotated[UploadFile, File(...)],
    chunking_strategy: Annotated[
        ChunkingStrategy,
        Query(description="Chunking strategy to use."),
    ] = "recursive",
) -> dict[str, object]:

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    file_extension = file.filename.lower().split(".")[-1]

    if file_extension not in {"pdf", "txt"}:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are supported.",
        )

    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )

    try:
        if file_extension == "pdf":
            text = extract_text_from_pdf(file_bytes)
        else:
            text = extract_text_from_txt(file_bytes)

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to extract text: {exc}",
        ) from exc

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="No text could be extracted from the document.",
        )

    chunks = chunk_text(
        text=text,
        strategy=chunking_strategy,
    )
    document_id = str(uuid4())

    embedding_service = EmbeddingService()
    vector_service = VectorService()

    embeddings = embedding_service.generate_embeddings(chunks)

    vector_service.create_collection()

    stored_chunks = vector_service.insert_chunks(
        vectors=embeddings,
        document_id=document_id,
        chunks=chunks,
    )
    db = SessionLocal()

    try:
        document = Document(
            id=document_id,
            filename=file.filename,
            file_type=file_extension,
            chunking_strategy=chunking_strategy,
            total_characters=len(text),
            chunks_count=stored_chunks,
        )

        db.add(document)
        db.commit()
    finally:
        db.close()

    return {
    "document_id": document_id,
    "filename": file.filename,
    "file_type": file_extension,
    "chunking_strategy": chunking_strategy,
    "total_characters": len(text),
    "chunks_created": len(chunks),
    "chunks_stored": stored_chunks,
}
