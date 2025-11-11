from app.llm.openai_client import OpenAIClient
from app.core.logger import logger


class CodeAgent:
    def __init__(self):
        self.openai_client = OpenAIClient()
        self.system_prompt = """You are a coding specialist.
You excel at writing code, debugging, explaining programming concepts, and technical implementations.
Provide clear code examples with explanations.
Use best practices and include comments in code."""

    def process(self, user_message: str, context: dict = None) -> str:
        messages = [{"role": "system", "content": self.system_prompt}]

        if context and context.get("context"):
            user_content = f"""Context from documents:
{context['context']}

Coding request: {user_message}"""
        else:
            user_content = user_message

        messages.append({"role": "user", "content": user_content})

        logger.info("Code agent processing request")
        response = self.openai_client.generate_response(messages)
        return response