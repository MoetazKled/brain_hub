from app.core.logger import logger


class TXTLoader:
    def load(self, file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()

            logger.info(f"Loaded TXT: {len(text)} characters")
            return text
        except Exception as e:
            logger.error(f"Error loading TXT: {e}")
            raise