from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from app.rag.vector_store import VectorStore
from app.core.config import settings

class RAGChain:
    def __init__(self):
        self.vector_store = VectorStore()
        self.retriever = self.vector_store.as_retriever()
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        template = """Answer based on context:

{context}

Question: {question}"""
        
        self.prompt = ChatPromptTemplate.from_template(template)
        
        self.chain = (
            {"context": self.retriever | self._format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
    
    def _format_docs(self, docs):
        return "\n\n".join([d.page_content for d in docs])
    
    def invoke(self, question: str):
        docs = self.retriever.get_relevant_documents(question)
        answer = self.chain.invoke(question)
        sources = list(set([d.metadata.get('source', 'Unknown') for d in docs]))
        return {"answer": answer, "sources": sources}