from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.core.config import settings

class ConversationalAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=settings.OPENAI_API_KEY)
        self.system_prompt = "You are a helpful assistant."
    
    def generate_response(self, user_message: str, history: list = None, context: dict = None):
        messages = [SystemMessage(content=self.system_prompt)]
        
        if history:
            for msg in history:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                else:
                    messages.append(AIMessage(content=msg["content"]))
        
        user_content = user_message
        if context and context.get("context"):
            user_content = f"Context:\n{context['context']}\n\nQuestion: {user_message}"
        
        messages.append(HumanMessage(content=user_content))
        
        response = self.llm.invoke(messages)
        sources = context.get("sources", []) if context else []
        return response.content, sources