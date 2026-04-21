from behave import given, when, then
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app, ai_provider
from models import QuizItem, UserSession, ChatMessage, SubmittedAnswer, EvaluationResult, QuizRequest
from database import engine
from sqlmodel import Session, SQLModel, select, delete

SQLModel.metadata.create_all(engine)



@given(u'a student session exists in the database')
def step_impl(context):
    context.client = TestClient(app)
    with Session(engine) as db_session:
        # Delete from leaf to root to respect FK constraints
        db_session.exec(delete(EvaluationResult))
        db_session.exec(delete(SubmittedAnswer))
        db_session.exec(delete(QuizItem))
        db_session.exec(delete(QuizRequest))
        db_session.exec(delete(ChatMessage))
        db_session.exec(delete(UserSession))
        db_session.commit()

        session = UserSession(id=1)          
        db_session.add(session)
        db_session.commit()

@given('the AI service is mocked to return an explanation "{explanation}"')
def step_impl(context, explanation):
    context.mock_ai = patch.object(ai_provider, 'get_explanation', return_value=explanation)
    context.mock_ai.start()

@given('the AI service is mocked to raise a connection error')
def step_impl(context):
    context.mock_ai = patch.object(ai_provider, 'get_explanation', side_effect=ConnectionError())
    context.mock_ai.start()


@when('the student sends a POST to /chat with content "{content}"')
def step_impl(context, content):
    response = context.client.post("/chat", json={"content": content, "session_id": getattr(context, 'session_id', 1)})
    context.response = response

@when(u'the student sends a POST to /chat with content ""')
def step_impl(context):
    response = context.client.post("/chat", json={"content": "", "session_id": getattr(context, 'session_id', 1)})
    context.response = response

@then('the response status code should be {status_code:d}')
def step_impl(context, status_code):
    assert context.response.status_code == status_code

@then('a ChatMessage should be created with role "{role}" and content "{content}"')
def step_impl(context, role, content):
    with Session(engine) as db_session:
        msg = db_session.exec(select(ChatMessage).where(ChatMessage.role == role, ChatMessage.content == content)).first()
        assert msg is not None

@then('the response should contain the message "{error_msg}"')
def step_impl(context, error_msg):
    print(context.response.json())
    assert error_msg in context.response.json().get("detail", "")

@then(u'no ChatMessage should be created in the database')
def step_impl(context):
    with Session(engine) as db_session:
        messages = db_session.exec(select(ChatMessage).where(ChatMessage.content == "")).all()
        assert len(messages) == 0

@then(u'a ChatMessage should be created with role "assistant" and content containing "{keyword}"')
def step_impl(context, keyword):
    with Session(engine) as db_session:
        msg = db_session.exec(select(ChatMessage).where(ChatMessage.role == "assistant")).first()
        assert msg is not None
        assert keyword in msg.content

def after_scenario(context, scenario):
    if hasattr(context, 'mock_ai'):
        context.mock_ai.stop()
    if hasattr(context, 'mock_eval'):
        context.mock_eval.stop()
    if hasattr(context, 'mock_quiz'):
        context.mock_quiz.stop()
    if hasattr(context, 'mock_explanation'):
        context.mock_explanation.stop()