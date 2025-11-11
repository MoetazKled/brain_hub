from docx import Document
from app.core.logger import logger


class DOCXLoader:
    def load(self, file_path: str) -> str:
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"

            logger.info(f"Loaded DOCX: {len(text)} characters")
            return text
        except Exception as e:
            logger.error(f"Error loading DOCX: {e}")
            raise