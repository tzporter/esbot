from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlmodel import Session
from pydantic import BaseModel
from contextlib import asynccontextmanager

from database import init_db, get_session
from ai_service import AIService

from models import QuizItem, QuizRequest, SubmittedAnswer, EvaluationResult

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


def safe_ai_call(fn, *args, max_retries=1):
    last_error = None
    for attempt in range(max_retries + 1):
        try:
            return fn(*args)
        except Exception as e:
            last_error = e

    if isinstance(last_error, ConnectionError):
        raise HTTPException(status_code=503, detail="AI service unavailable")
    else:
        raise HTTPException(status_code=500, detail=str(last_error))


# ==================================================
# DTOs
# ==================================================


class CreateSessionRequest(BaseModel):
    user_id: str = "anonymous"
    title: str | None = None


class MessageRequest(BaseModel):
    content: str


class QuizRequestModel(BaseModel):
    topic: str


class AnswerRequest(BaseModel):
    user_answer: str


api_router = APIRouter(prefix="/api/v1")

@api_router.get("/health")
def health_check():
    return {"status": "ok"}

# ==================================================
# 1. CREATE SESSION
# ==================================================


@api_router.post("/sessions")
def create_session(request: CreateSessionRequest, db: Session = Depends(get_session)):

    repo = get_repo(db)

    session = repo.create(user_id=request.user_id, title=request.title)

    return session


# ==================================================
# 2. LIST SESSIONS
# ==================================================


@api_router.get("/sessions")
def get_sessions(db: Session = Depends(get_session)):

    repo = get_repo(db)

    return repo.get_by_user("anonymous")


# ==================================================
# 3. GET SESSION MESSAGES
# ==================================================


@api_router.get("/sessions/{session_id}/messages")
def get_messages(session_id: int, db: Session = Depends(get_session)):

    repo = get_repo(db)

    session_obj = repo.get_by_id(session_id)

    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found")

    return repo.get_messages(session_id)


# ==================================================
# 4. SEND MESSAGE
# ==================================================


@api_router.post("/sessions/{session_id}/messages")
def send_message(
    session_id: int, request: MessageRequest, db: Session = Depends(get_session)
):

    if not request.content.strip():
        raise HTTPException(status_code=422, detail="Message cannot be empty")

    repo = get_repo(db)

    session_obj = repo.get_by_id(session_id)

    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found")

    # user message
    repo.append_message(session_id=session_id, content=request.content, role="user")

    # AI response
    ai_response = safe_ai_call(ai_provider.get_explanation, request.content)

    # assistant message
    repo.append_message(session_id=session_id, content=ai_response, role="assistant")

    return {"response": ai_response}


# ==================================================
# 5. GET SESSION QUIZZES
# ==================================================

@api_router.get("/sessions/{session_id}/quizzes")
def get_session_quizzes(session_id: int, db: Session = Depends(get_session)):
    repo = get_repo(db)
    try:
        quizzes = repo.get_quizzes(session_id)
        return {"quizzes": quizzes}
    except ValueError:
        raise HTTPException(status_code=404, detail="Session not found")

# ==================================================
# 6. QUIZ REQUEST (AI ONLY, NO REPO QUIZ TABLE USAGE REQUIRED)
# ==================================================


@api_router.post("/sessions/{session_id}/quiz")
def generate_quiz(
    session_id: int, request: QuizRequestModel, db: Session = Depends(get_session)
):
    repo = get_repo(db)
    session_obj = repo.get_by_id(session_id)

    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found")

    # 1. Fetch the quiz JSON structure from the AI or Mock service
    quiz_json = safe_ai_call(ai_provider.get_quiz, request.topic)

    # 2. Delegate database persistence to the repository layer by passing the session object
    raw_questions = quiz_json.get("quiz", {}).get("questions", [])
    saved_questions = repo.save_generated_quiz(
        session_obj=session_obj,  # Fixed: Passing the database object directly
        topic=request.topic, 
        questions=raw_questions
    )

    # 3. Return the response containing database-persisted QuizItem IDs
    return {
        "quiz": {
            "topic": quiz_json.get("quiz", {}).get("topic", request.topic),
            "questions": saved_questions
        }
    }

# ==================================================
# 6. ANSWER EVALUATION
# ==================================================


@api_router.post("/quiz-items/{quiz_item_id}/submit")
def submit_answer(
    quiz_item_id: int, request: AnswerRequest, db: Session = Depends(get_session)
):

    quiz_item = db.get(QuizItem, quiz_item_id)

    if not quiz_item:
        raise HTTPException(status_code=404, detail="Quiz item not found")

    submitted = SubmittedAnswer(
        user_answer=request.user_answer, quiz_item_id=quiz_item_id
    )

    db.add(submitted)
    db.commit()
    db.refresh(submitted)

    result = safe_ai_call(
        ai_provider.evaluate_answer,
        quiz_item.question_text,
        quiz_item.correct_answer,
        request.user_answer,
    )

    if result.get("needs_clarification"):
        return {
            "submitted_answer_id": submitted.id,
            "needs_clarification": True,
            "clarification_question": result["clarification_question"],
        }

    evaluation = EvaluationResult(
        is_correct=result["is_correct"],
        feedback=result["feedback"],
        submitted_answer_id=submitted.id,
    )

    db.add(evaluation)
    db.commit()

    return {
        "submitted_answer_id": submitted.id,
        "is_correct": result["is_correct"],
        "feedback": result["feedback"],
    }


# ==================================================
# 7. DELETE SESSION
# ==================================================


@api_router.delete("/sessions/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_session)):

    repo = get_repo(db)

    session_obj = repo.get_by_id(session_id)

    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found")

    repo.delete(session_id)

    return {"message": "Session deleted"}

app = FastAPI(lifespan=lifespan)
app.include_router(api_router)