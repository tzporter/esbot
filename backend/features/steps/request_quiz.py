from numpy import select
from requests import Session, delete

from models import QuizItem, QuizRequest, UserSession
from behave import given, when, then

# Feature: Request and Generate a Quiz
#   As a student
#   I want to request a quiz on a specific topic via the API
#   So that the system generates and returns practice questions for me

  # Background:
  #   Given a student session exists in the database

  # Scenario: Successfully request and receive a quiz on a valid topic

@given('a student session exists in the database')
def step_impl(context):
  with Session(engine) as db_session:
      db_session.exec(delete(UserSession))
      
      new_session = UserSession(id=1)
      db_session.add(new_session)
      db_session.commit()
      context.session_id = 1

@given('the AI service is mocked to return a structured quiz with question "Conjugate \'machen\' in present tense for \'ich\'" and answer "mache"')
def step_impl(context):
  # Mock the AI service to return a structured quiz response
  quiz_response = {
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
  context.mock_ai = patch.object(ai_provider, 'get_quiz', return_value=quiz_response)
@when('the student sends a POST to /chat with content "<content>" and quiz toggle is enabled')
def step_impl(context):
  # Send a POST request to the /chat endpoint with the specified content
  context.response = context.client.post('/chat', json={"content": context.content, "quiz_enabled": True})
@then('the response status code should be 200')
def step_impl(context):
  # Assert that the response status code is 200
  assert context.response.status_code == 200
@then('a QuizRequest should be created with topic "German verb conjugation"')
def step_impl(context):
  # Assert that a QuizRequest was created in the database with the correct topic
  with Session(engine) as db_session:
      quiz_request = db_session.exec(select(QuizRequest).where(QuizRequest.topic == "German verb conjugation")).first()
      assert quiz_request is not None
@then('a QuizItem should be created with question "Conjugate \'machen\' in present tense for \'ich\'"')
def step_impl(context):    # Assert that a QuizItem was created in the database with the correct question
  with Session(engine) as db_session:
      quiz_item = db_session.exec(select(QuizItem).where(QuizItem.question_text == "Conjugate 'machen' in present tense for 'ich'")).first()
      assert quiz_item is not None
@then('the QuizItem should have the correct answer "mache"')
def step_impl(context):    # Assert that the QuizItem has the correct answer
  with Session(engine) as db_session:
      quiz_item = db_session.exec(select(QuizItem).where(QuizItem.question_text == "Conjugate 'machen' in present tense for 'ich'")).first()
      assert quiz_item.correct_answer == "mache"



  # Scenario: Request a quiz without specifying a topic
  #   When the student sends a POST to /chat with content "Give me a quiz"
  #   Then the response status code should be 400
  #   And the response should contain the message "Please provide a topic for the quiz."
  #   And no QuizRequest should be created in the database

  # Scenario: AI model rejects a quiz prompt that violates safety guidelines
  #   Given the AI service is mocked to reject the prompt for safety reasons
  #   When the student sends a POST to /chat with content "Give me a quiz on something harmful"
  #   Then the response status code should be 422
  #   And the response should contain the message "Request rejected: content violates safety guidelines"
  #   And no QuizItem should be created in the database

  # Scenario: System retries when AI returns an unstructured quiz response
  #   Given the AI service is mocked to return unstructured text on the first call and a valid response on the second call
  #   When the student sends a POST to /chat with content "Give me a quiz on German verb conjugation"
  #   Then the response status code should be 200
  #   And a QuizItem should be created with a valid question and answer