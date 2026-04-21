from numpy import select
from requests import Session, delete

from models import QuizItem, QuizRequest, UserSession
from behave import given, when, then

from unittest.mock import patch
from main import ai_provider
from database import engine
from sqlmodel import Session, SQLModel, select, delete
import json

# Feature: Request and Generate a Quiz
#   As a student
#   I want to request a quiz on a specific topic via the API
#   So that the system generates and returns practice questions for me

  # Background:
  #   Given a student session exists in the database

  # Scenario: Successfully request and receive a quiz on a valid topic



@given('the AI service is mocked to return a structured quiz with question "{question}" and answer "{answer}"')
def step_impl(context, question, answer):
  quiz_response = {
    "quiz": {
      "topic": "General topic",
      "questions": [
        {
          "question": question,
          "answer": answer
        }
      ]
    }
  }
  context.mock_quiz = patch.object(ai_provider, 'get_quiz', return_value=quiz_response)
  context.mock_quiz.start()

@given('the AI service is mocked to return "{response}"')
def step_impl(context, response):
  error_response = {
    "status": "error",
    "message": "The quiz feature is not enabled. Please press the quiz button to enable it then try again."
  }
  context.mock_quiz = patch.object(ai_provider, 'get_quiz', return_value=error_response)
  context.mock_explanation = patch.object(ai_provider, 'get_explanation', return_value=json.dumps(error_response))
  context.mock_quiz.start()
  context.mock_explanation.start()
  


@when('the student sends a POST to /quiz-request with content "{content}"')
def step_impl(context, content):
  context.response = context.client.post('/quiz-request', json={"topic": str(content), "session_id": getattr(context, 'session_id', 1)})

@when('the student sends a POST to /quiz-request with no content')
def step_impl(context):
  context.response = context.client.post('/quiz-request', json={"session_id": getattr(context, 'session_id', 1)})

@then('a QuizRequest should be created with topic "{topic}"')
def step_impl(context, topic):
  with Session(engine) as db_session:
      quiz_request = db_session.exec(select(QuizRequest).where(QuizRequest.topic == topic)).first()
      assert quiz_request is not None
      context.quiz_request_id = quiz_request.id

@then('a QuizItem should be created with question "{question}"')
def step_impl(context, question):
  with Session(engine) as db_session:
      quiz_item = db_session.exec(select(QuizItem).where(QuizItem.quiz_request_id == context.quiz_request_id)).first()
      context.quiz_item_id = quiz_item.id
      assert quiz_item.question_text == question

@then('the QuizItem should have the correct answer "{answer}"')
def step_impl(context, answer):
  with Session(engine) as db_session:
      quiz_item = db_session.exec(select(QuizItem).where(QuizItem.id == context.quiz_item_id)).first()
      assert quiz_item.correct_answer == answer

@then('no QuizRequest should be created in the database')
def step_impl(context):
  with Session(engine) as db_session:
      requests = db_session.exec(select(QuizRequest)).all()
      assert len(requests) == 0

@given('the AI service is mocked to reject the prompt for safety reasons')
def step_impl(context):
  context.mock_quiz = patch.object(ai_provider, 'get_quiz', side_effect=Exception("content violates safety guidelines"))
  context.mock_quiz.start()

@then('no QuizItem should be created in the database')
def step_impl(context):
  with Session(engine) as db_session:
      items = db_session.exec(select(QuizItem)).all()
      assert len(items) == 0

@given('the AI service is mocked to return unstructured text on the first call and a valid response on the second call')
def step_impl(context):
  valid_response = {
    "quiz": {
      "topic": "German verb conjugation",
      "questions": [
        {
          "question": "Conjugate 'machen' in present tense for 'ich'",
          "answer": "mache"
        }
      ]
    }
  }
  context.mock_quiz = patch.object(ai_provider, 'get_quiz', side_effect=[Exception("Unstructured format"), valid_response])
  context.mock_quiz.start()

@then('a QuizItem should be created with a valid question and answer')
def step_impl(context):
  with Session(engine) as db_session:
      quiz_item = db_session.exec(select(QuizItem)).first()
      assert quiz_item is not None
      assert quiz_item.question_text != ""
      assert quiz_item.correct_answer != ""