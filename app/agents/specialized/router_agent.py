from app.llm.openai_client import OpenAIClient
from app.core.logger import logger


class RouterAgent:
    def __init__(self):
        self.openai_client = OpenAIClient()

    def route(self, user_message: str) -> str:
        prompt = f"""You are a router. Analyze this message and decide which agent should handle it.

Available agents:
- research: For questions, research, finding information, general knowledge
- code: For programming, coding, debugging, technical implementation
- summary: For summarizing text, documents, or creating concise overviews

Message: "{user_message}"

Respond with ONLY ONE WORD: research, code, or summary"""

        messages = [
            {"role": "system", "content": "You are a routing assistant."},
            {"role": "user", "content": prompt}
        ]

        response = self.openai_client.generate_response(messages)
        agent_type = response.strip().lower()

        if agent_type not in ["research", "code", "summary"]:
            agent_type = "research"

        logger.info(f"Routed to: {agent_type}")
        return agent_type