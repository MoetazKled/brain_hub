from app.llm.openai_client import OpenAIClient
from app.core.logger import logger


class ConversationalAgent:
    def __init__(self):
        self.openai_client = OpenAIClient()
        self.system_prompt = """You are a helpful AI assistant. 
You provide clear, friendly, and accurate responses.
Keep your answers concise and helpful."""

    def generate_response(self, user_message: str, conversation_history: list = None) -> str:
        messages = [{"role": "system", "content": self.system_prompt}]

        if conversation_history:
            for msg in conversation_history:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        messages.append({"role": "user", "content": user_message})

        logger.info(f"Sending {len(messages)} messages to OpenAI")
        response = self.openai_client.generate_response(messages)

        return response