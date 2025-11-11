from app.llm.openai_client import OpenAIClient
from app.core.logger import logger


class SummaryAgent:
    def __init__(self):
        self.openai_client = OpenAIClient()
        self.system_prompt = """You are a summarization specialist.
You excel at condensing information, creating concise overviews, and extracting key points.
Keep summaries clear, structured, and easy to understand.
Highlight the most important information."""

    def process(self, user_message: str, context: dict = None) -> str:
        messages = [{"role": "system", "content": self.system_prompt}]

        if context and context.get("context"):
            user_content = f"""Content to summarize:
{context['context']}

Additional instructions: {user_message}"""
        else:
            user_content = user_message

        messages.append({"role": "user", "content": user_content})

        logger.info("Summary agent processing request")
        response = self.openai_client.generate_response(messages)
        return response