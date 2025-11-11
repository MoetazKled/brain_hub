from app.llm.openai_client import OpenAIClient
from app.core.logger import logger


class ResearchAgent:
    def __init__(self):
        self.openai_client = OpenAIClient()
        self.system_prompt = """You are a research specialist.
You excel at finding information, answering questions, and providing detailed explanations.
Use the provided context from documents when available.
Be thorough and cite sources when using document information."""

    def process(self, user_message: str, context: dict = None) -> str:
        messages = [{"role": "system", "content": self.system_prompt}]

        if context and context.get("context"):
            user_content = f"""Context from documents:
{context['context']}

Question: {user_message}"""
        else:
            user_content = user_message

        messages.append({"role": "user", "content": user_content})

        logger.info("Research agent processing request")
        response = self.openai_client.generate_response(messages)
        return response