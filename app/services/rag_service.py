from sqlalchemy.orm import Session
from app.rag.vector_store import VectorStore

class RAGService:
    def __init__(self, db: Session):
        self.db = db
        self.vector_store = VectorStore()
    
    def get_context(self, query: str) -> dict:
        docs = self.vector_store.search(query, k=3)
        
        if not docs:
            return None
        
        context = "\n\n".join([f"From {d.metadata.get('source')}:\n{d.page_content}" for d in docs])
        sources = list(set([d.metadata.get('source') for d in docs]))
        
        return {"context": context, "sources": sources}