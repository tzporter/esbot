from behave import given, when, then
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app, ai_provider
from models import QuizItem, UserSession, ChatMessage, SubmittedAnswer, EvaluationResult, QuizRequest
from database import engine
from sqlmodel import Session, SQLModel, select, delete

SQLModel.metadata.create_all(engine)

client = TestClient(app)

@given('a student session exists in the database')
def step_impl(context):
    with Session(engine) as db_session:
        db_session.exec(delete(UserSession))
        
        new_session = UserSession(id=1)
        db_session.add(new_session)
        db_session.commit()
        context.session_id = 1
        
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
    response = client.post("/chat", json={"content": content, "session_id": getattr(context, 'session_id', 999)})
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
    assert error_msg in context.response.json().get("detail", "")

def after_scenario(context, scenario):
    if hasattr(context, 'mock_ai'):
        context.mock_ai.stop()


@when(u'the student sends a POST to /chat with content ""')
def step_impl(context):
    response = client.post("/chat", json={"content": "", "session_id": getattr(context, 'session_id', 1)})
    context.response = response

@then(u'no ChatMessage should be created in the database')
def step_impl(context):
    with Session(engine) as db_session:
        messages = db_session.exec(select(ChatMessage).where(ChatMessage.content == "")).all()
        assert len(messages) == 0

@then(u'a ChatMessage should be created with role "assistant" and content containing "accusative"')
def step_impl(context):
    with Session(engine) as db_session:
        msg = db_session.exec(select(ChatMessage).where(ChatMessage.role == "assistant")).first()
        assert msg is not None
        assert "accusative" in msg.content



@given(u'a QuizItem exists with question "Conjugate \'machen\' in present tense for \'ich\'" and correct answer "mache"')
def step_impl(context):
    with Session(engine) as db_session:
        quiz_item = QuizItem(question="Conjugate 'machen' in present tense for 'ich'", correct_answer="mache")
        db_session.add(quiz_item)
        db_session.commit()
        db_session.refresh(quiz_item)
        context.quiz_item_id = quiz_item.id

@given(u'the AI service is mocked to return an evaluation with is_correct true and feedback "Correct! \'Mache\' is the right conjugation of \'machen\' for \'ich\' in present tense."')
def step_impl(context):
    context.mock_eval = patch.object(ai_provider, 'get_explanation', return_value="True|Correct! 'Mache' is the right conjugation of 'machen' for 'ich' in present tense.")
    context.mock_eval.start()

@when(u'the student submits the answer "mache" to the quiz item')
def step_impl(context):
    response = client.post("/evaluate", json={"answer": "mache", "quiz_item_id": getattr(context, 'quiz_item_id', 1)})
    context.response = response

@then(u'a SubmittedAnswer should be created with user_answer "mache"')
def step_impl(context):
    with Session(engine) as db_session:
        ans = db_session.exec(select(SubmittedAnswer).where(SubmittedAnswer.user_answer == "mache")).first()
        assert ans is not None

@then(u'an EvaluationResult should be created with is_correct true')
def step_impl(context):
    with Session(engine) as db_session:
        eval_res = db_session.exec(select(EvaluationResult).where(EvaluationResult.is_correct == True)).first()
        assert eval_res is not None

@then(u'the response should contain feedback "Correct! \'Mache\' is the right conjugation of \'machen\' for \'ich\' in present tense."')
def step_impl(context):
    assert "Correct! 'Mache' is the right conjugation of 'machen' for 'ich' in present tense." in context.response.text

@given(u'the AI service is mocked to return a clarification request with message "Did you mean \'mache\' or \'machte\'? Please clarify."')
def step_impl(context):
    context.mock_eval = patch.object(ai_provider, 'get_explanation', return_value="Clarify|Did you mean 'mache' or 'machte'? Please clarify.")
    context.mock_eval.start()

@when(u'the student submits the answer "mach" to the quiz item')
def step_impl(context):
    response = client.post("/evaluate", json={"answer": "mach", "quiz_item_id": getattr(context, 'quiz_item_id', 1)})
    context.response = response

@then(u'a SubmittedAnswer should be created with user_answer "mach"')
def step_impl(context):
    with Session(engine) as db_session:
        ans = db_session.exec(select(SubmittedAnswer).where(SubmittedAnswer.user_answer == "mach")).first()
        assert ans is not None

@then(u'the response should contain a clarification question "Did you mean \'mache\' or \'machte\'? Please clarify."')
def step_impl(context):
    assert "Did you mean 'mache' or 'machte'? Please clarify." in context.response.text

@given(u'the AI service is mocked to fail on the first evaluation call and succeed on the second')
def step_impl(context):
    # İlk çağrıda hata, ikincide başarılı sonuç dönecek şekilde mock'luyoruz
    context.mock_eval = patch.object(ai_provider, 'get_explanation', side_effect=[ConnectionError(), "True|Good job!"])
    context.mock_eval.start()

@then(u'the response should contain feedback')
def step_impl(context):
    assert "feedback" in context.response.text.lower() or context.response.status_code == 200

@given(u'the AI service is mocked to return a structured quiz with question "Conjugate \'machen\' in present tense for \'ich\'" and answer "mache"')
def step_impl(context):
    context.mock_quiz = patch.object(ai_provider, 'get_explanation', return_value="Q: Conjugate 'machen' in present tense for 'ich' | A: mache")
    context.mock_quiz.start()

@then(u'a QuizRequest should be created with topic "German verb conjugation"')
def step_impl(context):
    with Session(engine) as db_session:
        req = db_session.exec(select(QuizRequest).where(QuizRequest.topic == "German verb conjugation")).first()
        assert req is not None

@then(u'a QuizItem should be created with question "Conjugate \'machen\' in present tense for \'ich\'"')
def step_impl(context):
    with Session(engine) as db_session:
        item = db_session.exec(select(QuizItem).where(QuizItem.question.contains("Conjugate 'machen'"))).first()
        assert item is not None

@then(u'the QuizItem should have the correct answer "mache"')
def step_impl(context):
    with Session(engine) as db_session:
        item = db_session.exec(select(QuizItem).where(QuizItem.correct_answer == "mache")).first()
        assert item is not None

@then(u'no QuizRequest should be created in the database')
def step_impl(context):
    with Session(engine) as db_session:
        reqs = db_session.exec(select(QuizRequest)).all()
        assert len(reqs) == 0

@given(u'the AI service is mocked to reject the prompt for safety reasons')
def step_impl(context):
    context.mock_quiz = patch.object(ai_provider, 'get_explanation', return_value="REJECTED|content violates safety guidelines")
    context.mock_quiz.start()

@then(u'no QuizItem should be created in the database')
def step_impl(context):
    with Session(engine) as db_session:
        items = db_session.exec(select(QuizItem)).all()
        assert len(items) == 0

@given(u'the AI service is mocked to return unstructured text on the first call and a valid response on the second call')
def step_impl(context):
    context.mock_quiz = patch.object(ai_provider, 'get_explanation', side_effect=["Bad formatting", "Q: Valid Question | A: Valid Answer"])
    context.mock_quiz.start()

@then(u'a QuizItem should be created with a valid question and answer')
def step_impl(context):
    with Session(engine) as db_session:
        items = db_session.exec(select(QuizItem)).all()
        assert len(items) > 0