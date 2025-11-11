from sqlalchemy.orm import Session
import uuid
from pathlib import Path
from app.database.models import Document, DocumentChunk
from app.rag.loaders.pdf_loader import PDFLoader
from app.rag.loaders.docx_loader import DOCXLoader
from app.rag.loaders.txt_loader import TXTLoader
from app.rag.processors.text_splitter import TextSplitter
from app.rag.embeddings.embedder import Embedder
from app.core.logger import logger


class RAGPipeline:
    def __init__(self, db: Session):
        self.db = db
        self.pdf_loader = PDFLoader()
        self.docx_loader = DOCXLoader()
        self.txt_loader = TXTLoader()
        self.text_splitter = TextSplitter()
        self.embedder = Embedder()

    def process_file(self, file_path: str, filename: str, file_type: str, user_id: str = None):
        logger.info(f"Processing file: {filename}")

        if file_type == "pdf":
            text = self.pdf_loader.load(file_path)
        elif file_type == "docx":
            text = self.docx_loader.load(file_path)
        elif file_type == "txt":
            text = self.txt_loader.load(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

        document = Document(
            filename=filename,
            file_path=file_path,
            file_type=file_type,
            user_id=user_id
        )
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)

        chunks = self.text_splitter.split(text)
        embeddings = self.embedder.embed_batch(chunks)

        for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            doc_chunk = DocumentChunk(
                document_id=document.id,
                content=chunk,
                chunk_index=idx,
                embedding=embedding
            )
            self.db.add(doc_chunk)

        self.db.commit()

        logger.info(f"File processed: {len(chunks)} chunks created")

        return {
            "document_id": str(document.id),
            "chunks_created": len(chunks)
        }