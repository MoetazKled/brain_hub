from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.rag.vector_store import VectorStore
from app.database.models import Document
from sqlalchemy.orm import Session

class DocumentProcessor:
    def __init__(self, db: Session):
        self.db = db
        self.vector_store = VectorStore()
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    
    def process_file(self, file_path: str, filename: str, user_id: str = None):
        if filename.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif filename.endswith('.docx'):
            loader = Docx2txtLoader(file_path)
        else:
            loader = TextLoader(file_path)
        
        documents = loader.load()
        
        for doc in documents:
            doc.metadata['source'] = filename
        
        chunks = self.splitter.split_documents(documents)
        
        self.vector_store.add_documents(chunks)
        
        doc_record = Document(
            filename=filename,
            file_path=file_path,
            user_id=user_id
        )
        self.db.add(doc_record)
        self.db.commit()
        self.db.refresh(doc_record)
        
        return {"document_id": str(doc_record.id), "chunks": len(chunks)}