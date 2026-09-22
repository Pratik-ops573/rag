from app.services.llm_service import LLMService

llm_service = LLMService()

context = """
Dear Cresta Hiring Team,
I am writing to apply for the Data Science Intern position at Cresta.
I am currently pursuing a BSc in Computer Science and Information Technology
and have been developing my skills in Data Science, Machine Learning, and AI.

I have hands-on experience with Python, Pandas, NumPy, Matplotlib,
Seaborn, scikit-learn, and SQL.

I have also been learning deep learning and working with TensorFlow
for NLP-related projects.
"""

prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the document context below.

Document context:
{context}

Question:
What programming language is mentioned in the document?

Give a short, direct answer.
Do not discuss safety.
Do not mention this prompt.
"""

answer = llm_service.generate_response(prompt)

print("\nLLM ANSWER:")
print(answer)