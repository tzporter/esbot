from backend.models import QuizItem, QuizRequest, UserSession
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
    # Create a new user session in the database for testing
    new_session = UserSession()
    context.db_session.add(new_session)
    context.db_session.commit()
    context.db_session.refresh(new_session)
    context.session = new_session

  @given('the AI service is mocked to return a structured quiz with question "Conjugate \'machen\' in present tense for \'ich\'" and answer "mache"')
  def step_impl(context):
    # Mock the AI service to return a structured quiz response
    context.mock_ai_service_response({
      "quiz": {
        "topic": "German verb conjugation",
        "items": [
          {
            "question": "Conjugate 'machen' in present tense for 'ich'",
            "answer": "mache"
          }
        ]
      }
    })
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

    assert quiz_request is not None
  @then('a QuizItem should be created with question "Conjugate \'machen\' in present tense for \'ich\'"')
  def step_impl(context):    # Assert that a QuizItem was created in the database with the correct question

    assert quiz_item is not None
  @then('the QuizItem should have the correct answer "mache"')
  def step_impl(context):    # Assert that the QuizItem has the correct answer

    assert quiz_item.answer == "mache"



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