# Palm Mind RAG Backend

A backend project built for the Palm Mind AI assignment.

This project uses FastAPI to build a simple RAG system where users can upload PDF/TXT documents and ask questions about them.

## Features

* Upload PDF and TXT files
* Fixed and recursive text chunking
* Generate embeddings using `all-MiniLM-L6-v2`
* Store embeddings in Qdrant
* Store document information in SQLite
* RAG-based question answering
* Redis chat memory for multi-turn conversations
* Interview booking through chat
* Booking information stored in SQLite

## Tech Stack

* FastAPI
* Python
* Qdrant
* Redis
* SQLite + SQLAlchemy
* Sentence Transformers
* OpenRouter
* PyMuPDF

## Project Structure

```text
app/
├── api/
├── core/
├── models/
├── schemas/
├── services/
└── utils/

scripts/
tests/
```

## Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it and install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file using `.env.example` and add the required:

```text
QDRANT_URL
QDRANT_API_KEY
REDIS_URL
OPENROUTER_API_KEY
OPENROUTER_MODEL
```

Run the application:

```bash
uvicorn app.main:app --reload
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## APIs

### Upload Document

```text
POST /documents/upload
```

Supports:

```text
fixed
recursive
```

### Chat

```text
POST /chat
```

The same `session_id` can be used for multi-turn conversations.

### Booking

```text
POST /bookings
```

Interview booking can also be handled through the chat endpoint.

## Testing

Run:

```bash
pytest -q
```

Current result:

```text
4 passed
```

Manual testing scripts are available inside the `scripts/` folder.

## Notes

The project does not use FAISS, Chroma, or `RetrievalQAChain`.

`.env` and other local files are excluded from Git.
