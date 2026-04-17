# This file was created with AI assistance. AI was used to check the consistency with the use-case UC-001
# and to assist in brainstorming the best way to implement the feature.

Feature: Ask a Course Question
  As a student
  I want to ask a general course question via the API
  So that I receive a structured explanation from the AI

  Background:
    Given a student session exists in the database

  Scenario: Successfully ask a course question and receive an explanation
    Given the AI service is mocked to return an explanation "The accusative case in German is used for direct objects. For example, 'Ich sehe den Hund' - 'den Hund' is accusative."
    When the student sends a POST to /chat with content "Explain the accusative case in German"
    Then the response status code should be 200
    And a ChatMessage should be created with role "user" and content "Explain the accusative case in German"
    And a ChatMessage should be created with role "assistant" and content containing "accusative"

  Scenario: Ask an empty question
    When the student sends a POST to /chat with content ""
    Then the response status code should be 400
    And the response should contain the message "Message content cannot be empty"
    And no ChatMessage should be created in the database

  Scenario: Ask a course question when the AI service is unavailable
    Given the AI service is mocked to raise a connection error
    When the student sends a POST to /chat with content "What are German modal verbs?"
    Then the response status code should be 503
    And the response should contain the message "AI service is currently unavailable"
