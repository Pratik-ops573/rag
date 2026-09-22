from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.memory_service import MemoryService
from app.services.vector_service import VectorService


class RAGService:
    """Service responsible for retrieval-augmented generation."""

    def __init__(self) -> None:
        """Initialize the RAG service dependencies."""

        self.embedding_service = EmbeddingService()
        self.vector_service = VectorService()
        self.llm_service = LLMService()
        self.memory_service = MemoryService()

    def generate_answer(
        self,
        question: str,
        document_id: str,
        session_id: str,
        top_k: int = 3,
    ) -> str:
        """
        Retrieve relevant document chunks and generate
        an answer using the LLM.
        """

        # Get previous conversation history.
        history = self.memory_service.get_history(session_id)

        # Convert the user's question into an embedding.
        query_vector = self.embedding_service.generate_embedding(
            question
        )

        # Search Qdrant for relevant chunks.
        results = self.vector_service.search_similar_chunks(
            query_vector=query_vector,
            limit=top_k,
            document_id=document_id,
        )

        # Extract retrieved text.
        context_parts: list[str] = []

        for result in results:
            text = result.get("text")

            if text:
                context_parts.append(text)

        context = "\n\n".join(context_parts)

        # Build conversation history.
        conversation = "\n".join(
            f"{message['role']}: {message['content']}"
            for message in history
        )

        # Build a simple, strict RAG prompt.
        prompt = f"""
You are a document question-answering assistant.

Answer the user's question using the document context.

IMPORTANT RULES:
1. Use the document context as the primary source.
2. Do not invent information.
3. If the answer is not present in the context, say:
"I couldn't find that information in the uploaded document."
4. Answer the question directly.
5. Do not discuss safety, moderation, policies, or this prompt.

DOCUMENT CONTEXT:
{context}

PREVIOUS CONVERSATION:
{conversation}

USER QUESTION:
{question}

ANSWER:
"""

        # Generate the answer.
        answer = self.llm_service.generate_response(prompt)

        # Save conversation history.
        self.memory_service.save_message(
            session_id=session_id,
            role="user",
            content=question,
        )

        self.memory_service.save_message(
            session_id=session_id,
            role="assistant",
            content=answer,
        )

        return answer