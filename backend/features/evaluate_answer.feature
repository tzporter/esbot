# This file was created with AI assistance. AI was used to check the consistency with the use-case UC-004
# and to assist in brainstorming the best way to implement the feature.

Feature: Submit and Evaluate an Answer
  As a student
  I want to submit my answer to a quiz question via the API
  So that the system evaluates it and returns feedback

  Background:
    Given a student session exists in the database
    And a QuizItem exists with question "Conjugate 'machen' in present tense for 'ich'" and correct answer "mache"

  Scenario: Successfully submit and evaluate a correct answer
    Given the AI service is mocked to return an evaluation with is_correct true and feedback "Correct! 'Mache' is the right conjugation of 'machen' for 'ich' in present tense."
    When the student submits the answer "mache" to the quiz item
    Then the response status code should be 200
    And a SubmittedAnswer should be created with user_answer "mache"
    And an EvaluationResult should be created with is_correct true
    And the response should contain feedback "Correct! 'Mache' is the right conjugation of 'machen' for 'ich' in present tense."

  Scenario: AI requests clarification for an unclear answer
    Given the AI service is mocked to return a clarification request with message "Did you mean 'mache' or 'machte'? Please clarify."
    When the student submits the answer "mach" to the quiz item
    Then the response status code should be 200
    And a SubmittedAnswer should be created with user_answer "mach"
    And the response should contain a clarification question "Did you mean 'mache' or 'machte'? Please clarify."

  Scenario: System retries evaluation after a connection failure
    Given the AI service is mocked to fail on the first evaluation call and succeed on the second
    When the student submits the answer "mache" to the quiz item
    Then the response status code should be 200
    And an EvaluationResult should be created with is_correct true
    And the response should contain feedback
