from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from app.schemas.chat import ChatRequest, ChatResponse
from app.database.models import Conversation, Message
from app.agents.conversational_agent import ConversationalAgent
from app.core.logger import logger


class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.agent = ConversationalAgent()

    def process_message(self, request: ChatRequest) -> ChatResponse:
        # Get or create conversation
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

        # Get conversation history (last 10 messages)
        history_messages = self.db.query(Message).filter(
            Message.conversation_id == conversation.id
        ).order_by(Message.created_at.desc()).limit(10).all()

        history = []
        for msg in reversed(history_messages):
            history.append({
                "role": msg.role,
                "content": msg.content
            })

        # Save user message
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=request.message
        )
        self.db.add(user_message)
        self.db.commit()

        # Generate AI response
        logger.info(f"Generating AI response with {len(history)} history messages")
        response_text = self.agent.generate_response(request.message, history)

        # Save bot response
        bot_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=response_text
        )
        self.db.add(bot_message)
        self.db.commit()
        self.db.refresh(bot_message)

        logger.info(f"Conversation {conversation.id}: Response generated")

        return ChatResponse(
            response=response_text,
            conversation_id=str(conversation.id),
            message_id=str(bot_message.id),
            timestamp=datetime.utcnow()
        )