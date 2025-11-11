from openai import OpenAI
from app.core.config import settings
from app.core.logger import logger


class Embedder:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "text-embedding-3-small"

    def embed_text(self, text: str) -> list:
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=text
            )

            embedding = response.data[0].embedding
            logger.info(f"Created embedding: {len(embedding)} dimensions")
            return embedding

        except Exception as e:
            logger.error(f"Error creating embedding: {e}")
            raise

    def embed_batch(self, texts: list) -> list:
        embeddings = []
        for text in texts:
            embedding = self.embed_text(text)
            embeddings.append(embedding)

        logger.info(f"Created {len(embeddings)} embeddings")
        return embeddings