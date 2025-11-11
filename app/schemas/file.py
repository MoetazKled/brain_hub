from pydantic import BaseModel
from datetime import datetime

class FileUploadResponse(BaseModel):
    file_id: str
    filename: str
    file_type: str
    chunks_created: int
    uploaded_at: datetime

class FileListResponse(BaseModel):
    id: str
    filename: str
    file_type: str
    uploaded_at: datetime