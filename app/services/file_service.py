from sqlalchemy.orm import Session
from fastapi import UploadFile
import uuid
from pathlib import Path
from datetime import datetime
from app.rag.pipeline import RAGPipeline
from app.database.models import Document
from app.schemas.file import FileUploadResponse, FileListResponse
from app.core.logger import logger


class FileService:
    def __init__(self, db: Session):
        self.db = db
        self.upload_dir = Path("uploads")
        self.upload_dir.mkdir(exist_ok=True)

    async def upload_file(self, file: UploadFile, user_id: str = None) -> FileUploadResponse:
        file_ext = file.filename.split(".")[-1].lower()

        if file_ext not in ["pdf", "docx", "txt"]:
            raise ValueError("Only PDF, DOCX, and TXT files are supported")

        file_id = str(uuid.uuid4())
        file_path = self.upload_dir / f"{file_id}.{file_ext}"

        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        logger.info(f"File saved: {file_path}")

        pipeline = RAGPipeline(self.db)
        result = pipeline.process_file(
            str(file_path),
            file.filename,
            file_ext,
            user_id
        )

        return FileUploadResponse(
            file_id=result["document_id"],
            filename=file.filename,
            file_type=file_ext,
            chunks_created=result["chunks_created"],
            uploaded_at=datetime.utcnow()
        )

    def list_files(self, user_id: str = None) -> list:
        query = self.db.query(Document)
        if user_id:
            query = query.filter(Document.user_id == user_id)

        documents = query.order_by(Document.uploaded_at.desc()).all()

        return [
            FileListResponse(
                id=str(doc.id),
                filename=doc.filename,
                file_type=doc.file_type,
                uploaded_at=doc.uploaded_at
            )
            for doc in documents
        ]

    def delete_file(self, file_id: str) -> dict:
        doc = self.db.query(Document).filter(
            Document.id == uuid.UUID(file_id)
        ).first()

        if not doc:
            raise ValueError("File not found")

        self.db.delete(doc)
        self.db.commit()

        Path(doc.file_path).unlink(missing_ok=True)

        logger.info(f"File deleted: {file_id}")
        return {"message": "File deleted successfully"}