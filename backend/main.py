from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Field, Session, SQLModel, select
from database import init_db, get_session
from ai_service import AIService
from pydantic import BaseModel

from models import ChatMessage, QuizItem, QuizRequest, SubmittedAnswer, UserSession, EvaluationResult


from contextlib import asynccontextmanager

ai_provider = AIService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    print("Database initialized", flush=True)
    yield

app = FastAPI(lifespan=lifespan)

class SubmitAnswerRequest(BaseModel):
    user_answer: str
    session_id: int

def evaluate_with_retry(question: str, correct_answer: str, user_answer: str) -> dict:
    last_error = None
    for attempt in range(2):
        try:
            return ai_provider.evaluate_answer(question, correct_answer, user_answer)
        except ConnectionError as e:
            last_error = e
    raise last_error


@app.get("/history")
def get_history(session: Session = Depends(get_session)):
    return session.exec(select(ChatMessage)).all()
@app.post("/quiz-request")
def request_quiz(quiz_data: dict, session: Session = Depends(get_session)):
    topic = quiz_data.get("topic")
    session_id = quiz_data.get("session_id")

    if not topic:
        raise HTTPException(status_code=400, detail="Please provide a topic for the quiz.")

    db_session = session.get(UserSession, session_id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")

    try:
        quiz_request = QuizRequest(topic=topic, session_id=session_id)
        session.add(quiz_request)
        session.commit()
        session.refresh(quiz_request)

        quiz_json = ai_provider.get_quiz(topic)

        for quiz_item in quiz_json["quiz"]["questions"]:
            question = quiz_item["question"]
            answer = quiz_item["answer"]
            # Here you would create QuizItem instances and associate them with the QuizRequest
            # For example:
            new_quiz_item = QuizItem(question=question, answer=answer, quiz_request_id=quiz_request.id)
            session.add(new_quiz_item)

            session.commit()
            session.refresh(new_quiz_item)

        return quiz_json

    except ConnectionError:
        raise HTTPException(status_code=503, detail="AI service is currently unavailable")

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
    
@app.post("/quiz-items/{quiz_item_id}/submit")
def submit_answer(
    quiz_item_id: int,
    request: SubmitAnswerRequest,
    session: Session = Depends(get_session),
):
    # 1. Load the QuizItem
    quiz_item = session.get(QuizItem, quiz_item_id)
    if quiz_item is None:
        raise HTTPException(status_code=404, detail="QuizItem not found")

    # 2. Persist SubmittedAnswer before calling AI (so it always exists in DB)
    submitted = SubmittedAnswer(
        user_answer=request.user_answer,
        quiz_item_id=quiz_item_id,
    )
    session.add(submitted)
    session.commit()
    session.refresh(submitted)

    # 3. Call AI with automatic retry on ConnectionError
    try:
        result = evaluate_with_retry(
            question=quiz_item.question_text,
            correct_answer=quiz_item.correct_answer,
            user_answer=request.user_answer,
        )
    except ConnectionError:
        raise HTTPException(status_code=503, detail="AI service is currently unavailable")

    # 4a. Clarification path — no EvaluationResult written
    if result.get("needs_clarification"):
        return {
            "submitted_answer_id": submitted.id,
            "needs_clarification": True,
            "clarification_question": result["clarification_question"],
        }

    # 4b. Normal evaluation path — persist EvaluationResult
    evaluation = EvaluationResult(
        is_correct=result["is_correct"],
        feedback=result["feedback"],
        submitted_answer_id=submitted.id,
    )
    session.add(evaluation)
    session.commit()

    return {
        "submitted_answer_id": submitted.id,
        "is_correct": result["is_correct"],
        "feedback": result["feedback"],
    }