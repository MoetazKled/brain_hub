#!/bin/bash
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


#Test OpenAI Connection
curl -X POST "http://localhost:8000/chat/send" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Python?", "user_id": "user1"}'

