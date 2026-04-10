from fastapi import FastAPI, Depends
from sqlmodel import Field, Session, SQLModel, select
from database import init_db, get_session

from models import ChatMessage, UserSession


from contextlib import asynccontextmanager

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
async def chat(message: ChatMessage, session: Session = Depends(get_session)):
    
    new_session = UserSession()
    session.add(new_session)
    session.commit()
    session.refresh(new_session)

    
    message.session_id = new_session.id
    session.add(message)

    
    assistant_message = ChatMessage(
        content="hello, user!", 
        role="assistant", 
        session_id=new_session.id
    )
    session.add(assistant_message)

    session.commit()
    session.refresh(assistant_message)
    return assistant_message