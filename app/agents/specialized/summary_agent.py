from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.core.config import settings

class SummaryAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=settings.OPENAI_API_KEY)
        self.system_prompt = "You are a summarization specialist. Create concise summaries."
    
    def process(self, user_message: str, context: dict = None):
        messages = [SystemMessage(content=self.system_prompt)]
        
        if context and context.get("context"):
            user_content = f"Content:\n{context['context']}\n\nInstructions: {user_message}"
        else:
            user_content = user_message
        
        messages.append(HumanMessage(content=user_content))
        response = self.llm.invoke(messages)
        return response.content