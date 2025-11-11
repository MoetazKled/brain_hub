from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database.models import DocumentChunk, Document
from app.rag.embeddings.embedder import Embedder
from app.core.logger import logger


class Retriever:
    def __init__(self, db: Session):
        self.db = db
        self.embedder = Embedder()

    def retrieve(self, query: str, top_k: int = 3) -> list:
        query_embedding = self.embedder.embed_text(query)

        results = self.db.execute(
            text("""
                SELECT 
                    dc.content,
                    d.filename,
                    dc.embedding <=> :query_embedding as distance
                FROM document_chunks dc
                JOIN documents d ON dc.document_id = d.id
                ORDER BY distance
                LIMIT :limit
            """),
            {
                "query_embedding": str(query_embedding),
                "limit": top_k
            }
        ).fetchall()

        retrieved_docs = []
        for row in results:
            retrieved_docs.append({
                "content": row[0],
                "source": row[1],
                "distance": row[2]
            })

        logger.info(f"Retrieved {len(retrieved_docs)} relevant chunks")
        return retrieved_docs