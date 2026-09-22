from typing import Literal

from langchain_text_splitters import RecursiveCharacterTextSplitter


ChunkingStrategy = Literal["fixed", "recursive"]


def fixed_chunking(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[str]:
    """Split text into fixed-size chunks with overlap."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0.")

    if overlap < 0:
        raise ValueError("overlap cannot be negative.")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size.")

    chunks: list[str] = []

    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        start += chunk_size - overlap

    return chunks


def recursive_chunking(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[str]:
    """Split text recursively using meaningful text boundaries."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0.")

    if overlap < 0:
        raise ValueError("overlap cannot be negative.")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    return splitter.split_text(text)


def chunk_text(
    text: str,
    strategy: ChunkingStrategy,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[str]:
    """Chunk text using the selected strategy."""

    if strategy == "fixed":
        return fixed_chunking(
            text=text,
            chunk_size=chunk_size,
            overlap=overlap,
        )

    return recursive_chunking(
        text=text,
        chunk_size=chunk_size,
        overlap=overlap,
    )