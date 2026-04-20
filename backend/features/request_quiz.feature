# This file was created with AI assistance. AI was used to check the consistency with the use-case UC-002
# and to assist in brainstorming the best way to implement the feature.

Feature: Request and Generate a Quiz
  As a student
  I want to request a quiz on a specific topic via the API
  So that the system generates and returns practice questions for me

  Background:
    Given a student session exists in the database

  Scenario: Successfully request and receive a quiz on a valid topic
    Given the AI service is mocked to return a structured quiz with question "<question>" and answer "<answer>"
    When the student sends a POST to /chat with content "Give me a quiz on <topic>" and quiz toggle is enabled
    Then the response status code should be 200
    And a QuizRequest should be created with topic "<topic>"
    And a QuizItem should be created with question "<question>"
    And the QuizItem should have the correct answer "<answer>"
    
    Examples:
      | topic | question | answer |
      | German verb conjugation | Conjugate 'machen' in present tense for 'ich' | mache |
      | German noun gender | What is the gender of the noun 'Haus'? | das |
      | Spanish greetings | How do you say 'hello' in Spanish? | hola |
      

  Scenario: Request a quiz without specifying a topic
    When the student sends a POST to /chat with content "Give me a quiz" and quiz toggle is enabled
    Then the response status code should be 400
    And the response should contain the message "Please provide a topic for the quiz."
    And no QuizRequest should be created in the database

  Scenario: Request a quiz without enabling quiz toggle
    When the student sends a POST to /chat with content "Give me a quiz" and quiz toggle is disabled
    Then the response status code should be 200
    And the response should contain the message "The quiz feature is not enabled. Please press the quiz button to enable it then try again."
    And no QuizRequest should be created in the database

  Scenario: AI model rejects a quiz prompt that violates safety guidelines
    Given the AI service is mocked to reject the prompt for safety reasons
    When the student sends a POST to /chat with content "Give me a quiz on something harmful" and quiz toggle is enabled
    Then the response status code should be 422
    And the response should contain the message "Request rejected: content violates safety guidelines"
    And no QuizItem should be created in the database

  Scenario: System retries when AI returns an unstructured quiz response
    Given the AI service is mocked to return unstructured text on the first call and a valid response on the second call
    When the student sends a POST to /chat with content "Give me a quiz on German verb conjugation" and quiz toggle is enabled
    Then the response status code should be 200
    And a QuizItem should be created with a valid question and answer