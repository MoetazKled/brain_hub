from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logger import logger
from app.database.connection import init_db
from app.api import chat, files

app = FastAPI(
    title="brain",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    logger.info("Starting brain v3...")
    init_db()
    logger.info("Database initialized")

app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(files.router, prefix="/files", tags=["Files"])

@app.get("/")
async def root():
    return {"message": "brain v3.0 with RAG", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}