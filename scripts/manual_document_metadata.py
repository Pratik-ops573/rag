from app.models.database import SessionLocal
from app.models.document import Document

document_id = "e815becb-e781-4585-b0ba-518589439ad8"

db = SessionLocal()

try:
    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if document:
        print("DOCUMENT FOUND")
        print("ID:", document.id)
        print("Filename:", document.filename)
        print("File type:", document.file_type)
        print("Chunking strategy:", document.chunking_strategy)
        print("Total characters:", document.total_characters)
        print("Chunks count:", document.chunks_count)
        print("Created at:", document.created_at)
    else:
        print("DOCUMENT NOT FOUND")

finally:
    db.close()