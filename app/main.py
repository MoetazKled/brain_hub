from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logger import logger
from app.database.connection import init_db
from app.api import chat

app = FastAPI(
    title="Chatbot Backend",
    version="1.0.0"
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
    logger.info("Starting chatbot backend...")
    init_db()
    logger.info("Database initialized")

app.include_router(chat.router, prefix="/chat", tags=["Chat"])

@app.get("/")
async def root():
    return {"message": "Chatbot Backend v1.0", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}