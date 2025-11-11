from pypdf import PdfReader
from app.core.logger import logger


class PDFLoader:
    def load(self, file_path: str) -> str:
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"

            logger.info(f"Loaded PDF: {len(text)} characters")
            return text
        except Exception as e:
            logger.error(f"Error loading PDF: {e}")
            raise