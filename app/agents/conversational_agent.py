from app.llm.openai_client import OpenAIClient
from app.core.logger import logger


class ConversationalAgent:
    def __init__(self):
        self.openai_client = OpenAIClient()
        self.system_prompt = """You are a helpful AI assistant.
When provided with context from documents, use that information to answer questions.
Always cite the source when using information from documents.
If the context doesn't contain relevant information, say so and provide a general answer."""

    def generate_response(self, user_message: str, conversation_history: list = None,
                          rag_context: dict = None) -> tuple:
        messages = [{"role": "system", "content": self.system_prompt}]

        if conversation_history:
            for msg in conversation_history:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        user_content = user_message

        if rag_context and rag_context.get("context"):
            user_content = f"""Context from documents:
{rag_context['context']}

Question: {user_message}"""

        messages.append({"role": "user", "content": user_content})

        logger.info(f"Sending {len(messages)} messages to OpenAI (RAG: {bool(rag_context)})")
        response = self.openai_client.generate_response(messages)

        sources = rag_context.get("sources", []) if rag_context else []

        return response, sources