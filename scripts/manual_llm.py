from app.services.llm_service import LLMService


llm_service = LLMService()

response = llm_service.generate_response(
    "Explain machine learning in two simple sentences."
)

print("Gemini response:")
print(response)
