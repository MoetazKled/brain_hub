from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from app.core.config import settings

class VectorStore:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
        self.vectorstore = Chroma(
            persist_directory="./chroma_db",
            embedding_function=self.embeddings
        )
    
    def add_documents(self, documents):
        self.vectorstore.add_documents(documents)
    
    def search(self, query, k=3):
        return self.vectorstore.similarity_search(query, k=k)
    
    def as_retriever(self):
        return self.vectorstore.as_retriever(search_kwargs={"k": 3})