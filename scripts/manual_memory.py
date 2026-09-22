from app.services.memory_service import MemoryService


memory_service = MemoryService()

session_id = "test-session-001"

memory_service.clear_history(session_id)

memory_service.save_message(
    session_id=session_id,
    role="user",
    content="My name is Pratik.",
)

memory_service.save_message(
    session_id=session_id,
    role="assistant",
    content="Nice to meet you, Pratik.",
)

memory_service.save_message(
    session_id=session_id,
    role="user",
    content="What is my name?",
)

history = memory_service.get_history(session_id)

print("\nChat history:\n")

for message in history:
    print(f"{message['role']}: {message['content']}")