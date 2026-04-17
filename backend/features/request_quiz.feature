# This file was created with AI assistance. AI was used to check the consistency with the use-case UC-002
# and to assist in brainstorming the best way to implement the feature.

Feature: Request and Generate a Quiz
  As a student
  I want to request a quiz on a specific topic via the API
  So that the system generates and returns practice questions for me

  Background:
    Given a student session exists in the database

  Scenario: Successfully request and receive a quiz on a valid topic
    Given the AI service is mocked to return a structured quiz with question "Conjugate 'machen' in present tense for 'ich'" and answer "mache"
    When the student sends a POST to /chat with content "Give me a quiz on German verb conjugation"
    Then the response status code should be 200
    And a QuizRequest should be created with topic "German verb conjugation"
    And a QuizItem should be created with question "Conjugate 'machen' in present tense for 'ich'"
    And the QuizItem should have the correct answer "mache"

  Scenario: Request a quiz without specifying a topic
    When the student sends a POST to /chat with content "Give me a quiz"
    Then the response status code should be 400
    And the response should contain the message "Please provide a topic for the quiz."
    And no QuizRequest should be created in the database

  Scenario: AI model rejects a quiz prompt that violates safety guidelines
    Given the AI service is mocked to reject the prompt for safety reasons
    When the student sends a POST to /chat with content "Give me a quiz on something harmful"
    Then the response status code should be 422
    And the response should contain the message "Request rejected: content violates safety guidelines"
    And no QuizItem should be created in the database

  Scenario: System retries when AI returns an unstructured quiz response
    Given the AI service is mocked to return unstructured text on the first call and a valid response on the second call
    When the student sends a POST to /chat with content "Give me a quiz on German verb conjugation"
    Then the response status code should be 200
    And a QuizItem should be created with a valid question and answer