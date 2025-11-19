from sqlalchemy.orm import Session
from fastapi import UploadFile
import uuid
from pathlib import Path
from datetime import datetime
from app.rag.document_processor import DocumentProcessor
from app.database.models import Document
from app.schemas.file import FileUploadResponse, FileListResponse

class FileService:
    def __init__(self, db: Session):
        self.db = db
        self.processor = DocumentProcessor(db)
        self.upload_dir = Path("uploads")
        self.upload_dir.mkdir(exist_ok=True)
    
    async def upload_file(self, file: UploadFile, user_id: str = None):
        file_ext = file.filename.split(".")[-1].lower()
        if file_ext not in ["pdf", "docx", "txt"]:
            raise ValueError("Only PDF, DOCX, TXT supported")
        
        file_id = str(uuid.uuid4())
        file_path = self.upload_dir / f"{file_id}.{file_ext}"
        
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        result = self.processor.process_file(str(file_path), file.filename, user_id)
        
        return FileUploadResponse(
            file_id=result["document_id"],
            filename=file.filename,
            file_type=file_ext,
            chunks_created=result["chunks"],
            uploaded_at=datetime.utcnow()
        )
    
    def list_files(self, user_id: str = None):
        query = self.db.query(Document)
        if user_id:
            query = query.filter(Document.user_id == user_id)
        
        docs = query.order_by(Document.uploaded_at.desc()).all()
        
        return [FileListResponse(
            id=str(d.id),
            filename=d.filename,
            file_type=d.filename.split(".")[-1],
            uploaded_at=d.uploaded_at
        ) for d in docs]
    
    def delete_file(self, file_id: str):
        doc = self.db.query(Document).filter(Document.id == uuid.UUID(file_id)).first()
        if not doc:
            raise ValueError("File not found")
        
        self.db.delete(doc)
        self.db.commit()
        Path(doc.file_path).unlink(missing_ok=True)
        return {"message": "Deleted"}