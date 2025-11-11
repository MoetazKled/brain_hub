from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from app.schemas.chat import ChatRequest, ChatResponse
from app.database.models import Conversation, Message
from app.agents.multi_agent_orchestrator import MultiAgentOrchestrator
from app.services.rag_service import RAGService
from app.core.logger import logger


class MultiAgentService:
    def __init__(self, db: Session):
        self.db = db
        self.orchestrator = MultiAgentOrchestrator()
        self.rag_service = RAGService(db)

    def process_message(self, request: ChatRequest) -> ChatResponse:
        if request.conversation_id:
            try:
                conv_id = uuid.UUID(request.conversation_id)
                conversation = self.db.query(Conversation).filter(
                    Conversation.id == conv_id
                ).first()
            except:
                conversation = None
        else:
            conversation = None

        if not conversation:
            conversation = Conversation(user_id=request.user_id)
            self.db.add(conversation)
            self.db.commit()
            self.db.refresh(conversation)
            logger.info(f"Created new conversation: {conversation.id}")

        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=request.message
        )
        self.db.add(user_message)
        self.db.commit()

        rag_context = None
        sources = None
        if request.use_rag:
            rag_context = self.rag_service.get_context(request.message)
            if rag_context:
                sources = rag_context.get("sources", [])

        logger.info(f"Processing with multi-agent (RAG: {bool(rag_context)})")
        response_text, agents_used = self.orchestrator.process(
            request.message,
            rag_context
        )

        bot_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=response_text
        )
        self.db.add(bot_message)
        self.db.commit()
        self.db.refresh(bot_message)

        return ChatResponse(
            response=response_text,
            conversation_id=str(conversation.id),
            message_id=str(bot_message.id),
            timestamp=datetime.utcnow(),
            sources=sources,
            agents_used=agents_used
        )