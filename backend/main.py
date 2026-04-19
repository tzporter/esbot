from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Field, Session, SQLModel, select
from database import init_db, get_session
from ai_service import AIService

from models import ChatMessage, UserSession


from contextlib import asynccontextmanager

ai_provider = AIService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    print("Database initialized", flush=True)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/history")
def get_history(session: Session = Depends(get_session)):
    return session.exec(select(ChatMessage)).all()

@app.post("/chat")
async def chat(message_data: dict, session: Session = Depends(get_session)):
    content = message_data.get("content", "")
    session_id = message_data.get("session_id")

    if not content.strip():
        raise HTTPException(status_code=400, detail="Message content cannot be empty")

    db_session = session.get(UserSession, session_id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")

    try:
        user_msg = ChatMessage(content=content, role="user", session_id=session_id)
        session.add(user_msg)
        
        response_content = ai_provider.get_explanation(content)
        
        assistant_msg = ChatMessage(content=response_content, role="assistant", session_id=session_id)
        session.add(assistant_msg)
        
        session.commit()
        session.refresh(assistant_msg)
        return assistant_msg

    except ConnectionError:
        raise HTTPException(status_code=503, detail="AI service is currently unavailable")