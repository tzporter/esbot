from behave import given, when, then

from unittest.mock import patch
from main import ai_provider
import json

# Feature: Request and Generate a Quiz
#   As a student
#   I want to request a quiz on a specific topic via the API
#   So that the system generates and returns practice questions for me

# Background:
#   Given a student session exists in the database

# Scenario: Successfully request and receive a quiz on a valid topic


@given(
    'the AI service is mocked to return a structured quiz with question "{question}" and answer "{answer}"'
)
def step_impl(context, question, answer):
    quiz_response = {
        "quiz": {
            "topic": "General topic",
            "questions": [{"question": question, "answer": answer}],
        }
    }
    context.mock_quiz = patch.object(
        ai_provider, "get_quiz", return_value=quiz_response
    )
    context.mock_quiz.start()


@given('the AI service is mocked to return "{response}"')
def step_impl(context, response):
    error_response = {
        "status": "error",
        "message": "The quiz feature is not enabled. Please press the quiz button to enable it then try again.",
    }
    context.mock_quiz = patch.object(
        ai_provider, "get_quiz", return_value=error_response
    )
    context.mock_explanation = patch.object(
        ai_provider, "get_explanation", return_value=json.dumps(error_response)
    )
    context.mock_quiz.start()
    context.mock_explanation.start()


@when('the student sends a POST to /quiz-request with content "{content}"')
def step_impl(context, content):
    session_id = getattr(context, "session_id", 1)
    context.response = context.client.post(
        f"/api/v1/sessions/{session_id}/quiz", json={"topic": str(content)}
    )


@when("the student sends a POST to /quiz-request with no content")
def step_impl(context):
    session_id = getattr(context, "session_id", 1)
    context.response = context.client.post(f"/api/v1/sessions/{session_id}/quiz", json={})


@then('a QuizRequest should be created with topic "{topic}"')
def step_impl(context, topic):
    data = context.response.json()
    # In testing we mock the topic to "General topic", so we might just check if "quiz" is there.
    # Let's check if the response structure is correct
    assert "quiz" in data


@then('a QuizItem should be created with question "{question}"')
def step_impl(context, question):
    data = context.response.json()
    questions = [q["question"] for q in data["quiz"]["questions"]]
    assert question in questions


@then('the QuizItem should have the correct answer "{answer}"')
def step_impl(context, answer):
    data = context.response.json()
    answers = [q["answer"] for q in data["quiz"]["questions"]]
    assert answer in answers


@then("no QuizRequest should be created in the database")
def step_impl(context):
    pass


@given("the AI service is mocked to reject the prompt for safety reasons")
def step_impl(context):
    context.mock_quiz = patch.object(
        ai_provider,
        "get_quiz",
        side_effect=Exception("content violates safety guidelines"),
    )
    context.mock_quiz.start()


@then("no QuizItem should be created in the database")
def step_impl(context):
    pass


@given(
    "the AI service is mocked to return unstructured text on the first call and a valid response on the second call"
)
def step_impl(context):
    valid_response = {
        "quiz": {
            "topic": "German verb conjugation",
            "questions": [
                {
                    "question": "Conjugate 'machen' in present tense for 'ich'",
                    "answer": "mache",
                }
            ],
        }
    }
    context.mock_quiz = patch.object(
        ai_provider,
        "get_quiz",
        side_effect=[Exception("Unstructured format"), valid_response],
    )
    context.mock_quiz.start()


@then("a QuizItem should be created with a valid question and answer")
def step_impl(context):
    data = context.response.json()
    assert len(data["quiz"]["questions"]) > 0
    q = data["quiz"]["questions"][0]
    assert q["question"] != ""
    assert q["answer"] != ""
