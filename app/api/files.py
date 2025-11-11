from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.services.file_service import FileService
from app.database.connection import get_db
from app.schemas.file import FileUploadResponse, FileListResponse

router = APIRouter()

@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    user_id: str = None,
    db: Session = Depends(get_db)
):
    try:
        file_service = FileService(db)
        result = await file_service.upload_file(file, user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list", response_model=list[FileListResponse])
async def list_files(user_id: str = None, db: Session = Depends(get_db)):
    file_service = FileService(db)
    return file_service.list_files(user_id)

@router.delete("/{file_id}")
async def delete_file(file_id: str, db: Session = Depends(get_db)):
    try:
        file_service = FileService(db)
        return file_service.delete_file(file_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/health")
async def health():
    return {"status": "healthy"}