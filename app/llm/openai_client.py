from openai import OpenAI
from app.core.config import settings
from app.core.logger import logger


class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4o-mini"

    def generate_response(self, messages: list) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )

            content = response.choices[0].message.content
            logger.info(f"OpenAI response generated: {len(content)} chars")
            return content

        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise