from app.services.chunking_service import (
    chunk_text,
    fixed_chunking,
    recursive_chunking,
)


def test_fixed_chunking() -> None:
    text = "A" * 1200

    chunks = fixed_chunking(
        text=text,
        chunk_size=500,
        overlap=50,
    )

    assert len(chunks) > 1
    assert all(len(chunk) <= 500 for chunk in chunks)


def test_recursive_chunking() -> None:
    text = (
        "Python is a programming language.\n\n"
        "Machine learning uses data to learn patterns.\n\n"
        "RAG combines retrieval with language models."
    )

    chunks = recursive_chunking(
        text=text,
        chunk_size=100,
        overlap=20,
    )

    assert len(chunks) > 1
    assert all(chunk.strip() for chunk in chunks)


def test_chunk_text_fixed() -> None:
    text = "A" * 1000

    chunks = chunk_text(
        text=text,
        strategy="fixed",
    )

    assert len(chunks) > 1


def test_chunk_text_recursive() -> None:
    text = (
        "Python is useful.\n\n"
        "Machine learning is powerful."
    )

    chunks = chunk_text(
        text=text,
        strategy="recursive",
    )

    assert len(chunks) >= 1