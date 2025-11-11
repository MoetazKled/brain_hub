from sqlalchemy.orm import Session
from app.rag.retrieval.retriever import Retriever
from app.core.logger import logger


class RAGService:
    def __init__(self, db: Session):
        self.db = db
        self.retriever = Retriever(db)

    def get_context(self, query: str) -> dict:
        retrieved_docs = self.retriever.retrieve(query, top_k=3)

        if not retrieved_docs:
            return None

        context = "\n\n".join([
            f"From {doc['source']}:\n{doc['content']}"
            for doc in retrieved_docs
        ])

        sources = list(set([doc['source'] for doc in retrieved_docs]))

        logger.info(f"Retrieved context from {len(sources)} documents")

        return {
            "context": context,
            "sources": sources
        }