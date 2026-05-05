from behave import given, when, then
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app, ai_provider
from models import QuizItem, QuizRequest, SubmittedAnswer, EvaluationResult
from database import engine
from sqlmodel import Session, SQLModel, select, delete

SQLModel.metadata.create_all(engine)

client = TestClient(app)


# Given

@given('a QuizItem exists with question "{question}" and correct answer "{correct_answer}"')
def step_impl(context, question, correct_answer):
    with Session(engine) as db_session:
        # Clean up dependent tables first to avoid FK violations
        db_session.exec(delete(EvaluationResult))
        db_session.exec(delete(SubmittedAnswer))
        db_session.exec(delete(QuizItem))
        db_session.exec(delete(QuizRequest))
        db_session.commit()

        # Create a QuizRequest as parent
        quiz_request = QuizRequest(id=1, topic="German verbs", difficulty="medium", session_id=1)
        db_session.add(quiz_request)
        db_session.commit()
        db_session.refresh(quiz_request)

        # Create the QuizItem
        item = QuizItem(
            id=1,
            question_text=question,
            correct_answer=correct_answer,
            quiz_request_id=quiz_request.id,
        )
        db_session.add(item)
        db_session.commit()
        db_session.refresh(item)

        context.quiz_item_id = item.id


@given('the AI service is mocked to return an evaluation with is_correct {is_correct} and feedback "{feedback}"')
def step_impl(context, is_correct, feedback):
    is_correct_bool = is_correct.strip().lower() == "true"
    mock_result = {"is_correct": is_correct_bool, "feedback": feedback}
    context.mock_eval = patch.object(ai_provider, "evaluate_answer", return_value=mock_result)
    context.mock_eval.start()


@given('the AI service is mocked to return a clarification request with message "{message}"')
def step_impl(context, message):
    mock_result = {"needs_clarification": True, "clarification_question": message}
    context.mock_eval = patch.object(ai_provider, "evaluate_answer", return_value=mock_result)
    context.mock_eval.start()


@given("the AI service is mocked to fail on the first evaluation call and succeed on the second")
def step_impl(context):
    success_result = {
        "is_correct": True,
        "feedback": "Correct! 'Mache' is the right conjugation.",
    }
    context.mock_eval = patch.object(
        ai_provider,
        "evaluate_answer",
        side_effect=[ConnectionError("Service unavailable"), success_result],
    )
    context.mock_eval.start()


# When

@when('the student submits the answer "{user_answer}" to the quiz item')
def step_impl(context, user_answer):
    quiz_item_id = getattr(context, "quiz_item_id", 1)
    response = client.post(
        f"/quiz-items/{quiz_item_id}/submit",
        json={"user_answer": user_answer, "session_id": getattr(context, "session_id", 1)},
    )
    context.response = response


# Then

@then('a SubmittedAnswer should be created with user_answer "{user_answer}"')
def step_impl(context, user_answer):
    with Session(engine) as db_session:
        submitted = db_session.exec(
            select(SubmittedAnswer).where(SubmittedAnswer.user_answer == user_answer)
        ).first()
        assert submitted is not None, (
            f"Expected a SubmittedAnswer with user_answer='{user_answer}' but none was found"
        )


@then("an EvaluationResult should be created with is_correct {is_correct}")
def step_impl(context, is_correct):
    is_correct_bool = is_correct.strip().lower() == "true"
    with Session(engine) as db_session:
        evaluation = db_session.exec(
            select(EvaluationResult).where(EvaluationResult.is_correct == is_correct_bool)
        ).first()
        assert evaluation is not None, (
            f"Expected an EvaluationResult with is_correct={is_correct_bool} but none was found"
        )


@then('the response should contain feedback "{feedback}"')
def step_impl(context, feedback):
    body = context.response.json()
    assert feedback in body.get("feedback", ""), (
        f"Expected feedback to contain '{feedback}', got: {body.get('feedback')}"
    )


@then('the response should contain a clarification question "{clarification_question}"')
def step_impl(context, clarification_question):
    body = context.response.json()
    assert clarification_question in body.get("clarification_question", ""), (
        f"Expected clarification_question to contain '{clarification_question}', "
        f"got: {body.get('clarification_question')}"
    )


@then("the response should contain feedback")
def step_impl(context):
    body = context.response.json()
    feedback = body.get("feedback", "")
    assert feedback, f"Expected a non-empty 'feedback' field in the response, got: {body}"


# Cleanup

def after_scenario(context, scenario):
    for mock_attr in ("mock_eval", "mock_ai", "mock_quiz"):
        mock = getattr(context, mock_attr, None)
        if mock:
            mock.stop()
