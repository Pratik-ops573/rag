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
        a context-aware answer using conversation history.
        """

        # 1. Get previous conversation history from Redis.
        history = self.memory_service.get_history(session_id)

        # 2. Convert the current question into an embedding.
        query_vector = self.embedding_service.generate_embedding(
            question
        )

        # 3. Search Qdrant for relevant chunks.
        results = self.vector_service.search_similar_chunks(
            query_vector=query_vector,
            limit=top_k,
            document_id=document_id,
        )

        # 4. Build context from retrieved chunks.
        context = "\n\n".join(
            result["text"]
            for result in results
            if result.get("text")
        )

        # 5. Format previous conversation.
        conversation = "\n".join(
            f"{message['role']}: {message['content']}"
            for message in history
        )

        # 6. Build the custom RAG prompt.
        prompt = f"""
You are a helpful assistant answering questions about uploaded documents.

Use ONLY the information provided in the document context below.

You may use the conversation history to understand references
and follow-up questions.

If the answer cannot be found in the document context, say:
"I couldn't find that information in the uploaded documents."

Previous conversation:
{conversation}

Document context:
{context}

Current question:
{question}

Answer:
"""

        # 7. Generate the answer using the LLM.
        answer = self.llm_service.generate_response(prompt)

        # 8. Save the user message to Redis.
        self.memory_service.save_message(
            session_id=session_id,
            role="user",
            content=question,
        )

        # 9. Save the assistant response to Redis.
        self.memory_service.save_message(
            session_id=session_id,
            role="assistant",
            content=answer,
        )

        return answer