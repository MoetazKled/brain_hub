from langchain_openai import ChatOpenAI
from app.core.config import settings

class RouterAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=settings.OPENAI_API_KEY)
    
    def route(self, user_message: str) -> str:
        prompt = f"""Analyze this message and pick ONE agent: research, code, or summary

Message: {user_message}

Respond with ONLY: research OR code OR summary"""
        
        response = self.llm.invoke(prompt)
        agent_type = response.content.strip().lower()
        return agent_type if agent_type in ["research", "code", "summary"] else "research"