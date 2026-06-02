from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from contextlib import asynccontextmanager
import json

from database import init_db, get_session
from ai_service import AIService

from models import (
    UserSession,
    ChatMessage,
    QuizRequest,
    QuizItem,
    SubmittedAnswer,
    EvaluationResult
)

from repositories.session_repository import SessionRepository


# ==================================================
# INIT
# ==================================================

ai_provider = AIService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    print("Database initialized", flush=True)
    yield


app = FastAPI(lifespan=lifespan)


# ==================================================
# HELPERS
# ==================================================

def get_repo(db: Session):
    return SessionRepository(db)


def safe_ai_call(fn, *args):
    try:
        return fn(*args)
    except ConnectionError:
        raise HTTPException(status_code=503, detail="AI service unavailable")


# ==================================================
# DTOs
# ==================================================

from pydantic import BaseModel


class CreateSessionRequest(BaseModel):
    user_id: str = "anonymous"
    title: str | None = None


class MessageRequest(BaseModel):
    content: str


class QuizRequestModel(BaseModel):
    topic: str


class AnswerRequest(BaseModel):
    user_answer: str


# ==================================================
# 1. CREATE SESSION
# ==================================================

@app.post("/sessions")
def create_session(
    request: CreateSessionRequest,
    db: Session = Depends(get_session)
):

    repo = get_repo(db)

    session = repo.create(
        user_id=request.user_id,
        title=request.title
    )

    return session


# ==================================================
# 2. LIST SESSIONS
# ==================================================

@app.get("/sessions")
def get_sessions(db: Session = Depends(get_session)):

    repo = get_repo(db)

    return repo.get_by_user("anonymous")   


# ==================================================
# 3. GET SESSION MESSAGES
# ==================================================

@app.get("/sessions/{session_id}/messages")
def get_messages(
    session_id: int,
    db: Session = Depends(get_session)
):

    repo = get_repo(db)

    session_obj = repo.get_by_id(session_id)

    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found")

    return repo.get_messages(session_id)


# ==================================================
# 4. SEND MESSAGE
# ==================================================

@app.post("/sessions/{session_id}/messages")
def send_message(
    session_id: int,
    request: MessageRequest,
    db: Session = Depends(get_session)
):

    if not request.content.strip():
        raise HTTPException(status_code=422, detail="Message cannot be empty")

    repo = get_repo(db)

    session_obj = repo.get_by_id(session_id)

    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found")

    # user message
    repo.append_message(
        session_id=session_id,
        content=request.content,
        role="user"
    )

    # AI response
    ai_response = safe_ai_call(
        ai_provider.get_explanation,
        request.content
    )

    # assistant message
    repo.append_message(
        session_id=session_id,
        content=ai_response,
        role="assistant"
    )

    return {"response": ai_response}


# ==================================================
# 5. QUIZ REQUEST (AI ONLY, NO REPO QUIZ TABLE USAGE REQUIRED)
# ==================================================

@app.post("/sessions/{session_id}/quiz")
def generate_quiz(
    session_id: int,
    request: QuizRequestModel,
    db: Session = Depends(get_session)
):

    repo = get_repo(db)

    session_obj = repo.get_by_id(session_id)

    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found")

    quiz_json = safe_ai_call(
        ai_provider.get_quiz,
        request.topic
    )

    return quiz_json


# ==================================================
# 6. ANSWER EVALUATION
# ==================================================

@app.post("/quiz-items/{quiz_item_id}/submit")
def submit_answer(
    quiz_item_id: int,
    request: AnswerRequest,
    db: Session = Depends(get_session)
):

    quiz_item = db.get(QuizItem, quiz_item_id)

    if not quiz_item:
        raise HTTPException(status_code=404, detail="Quiz item not found")

    submitted = SubmittedAnswer(
        user_answer=request.user_answer,
        quiz_item_id=quiz_item_id
    )

    db.add(submitted)
    db.commit()
    db.refresh(submitted)

    result = safe_ai_call(
        ai_provider.evaluate_answer,
        quiz_item.question_text,
        quiz_item.correct_answer,
        request.user_answer
    )

    if result.get("needs_clarification"):
        return {
            "submitted_answer_id": submitted.id,
            "needs_clarification": True,
            "clarification_question": result["clarification_question"]
        }

    evaluation = EvaluationResult(
        is_correct=result["is_correct"],
        feedback=result["feedback"],
        submitted_answer_id=submitted.id
    )

    db.add(evaluation)
    db.commit()

    return {
        "submitted_answer_id": submitted.id,
        "is_correct": result["is_correct"],
        "feedback": result["feedback"]
    }


# ==================================================
# 7. DELETE SESSION
# ==================================================

@app.delete("/sessions/{session_id}")
def delete_session(
    session_id: int,
    db: Session = Depends(get_session)
):

    repo = get_repo(db)

    session_obj = repo.get_by_id(session_id)

    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found")

    repo.delete(session_id)

    return {"message": "Session deleted"}