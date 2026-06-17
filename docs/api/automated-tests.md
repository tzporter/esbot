# Automated API Tests

## Framework Choice

For our automated API tests, we selected **pytest** combined with **FastAPI TestClient**. 
- **pytest** is the default option for tests in python. It is also consistent with the other tests in our project.
- **FastAPI TestClient** is a tool provided by FastAPI to test API endpoints. It allows us to simulate HTTP requests to our API endpoints without needing to run an actual server over the network.

## How to Run the Test Suite

The automated API test suite is located in `backend/tests/`. To run the tests, you can execute the following command from the root of the project:

```bash
docker-compose run backend pytest tests/test_api_workflow.py
```

## Backend Configuration for Tests

1. **In-Memory Database**: Tests utilize an in-memory SQLite database (`sqlite://`) overriding the actual database session dependency (`get_session`).
2. **Setup/Teardown**: A `pytest.fixture(name="client")` creates the database tables (`SQLModel.metadata.create_all`) before each test execution, yields the `TestClient`, and drops the tables (`SQLModel.metadata.drop_all`) afterwards.
3. **Mocking AI Services**: To avoid slow LLM inferences, `unittest.mock.patch` is used to mock the AI provider methods (`get_explanation`, `get_quiz`, `evaluate_answer`) within the happy-path test, substituting mock JSON responses.

## Test Descriptions

Our API tests are split into the following groups and cover multiple scenarios:

### 1. Happy-Path Workflow
(`test_api_workflow_happy_path`)
This test simulates a sequential workflow of an end user interacting with the ESBot API successfully:
- Verifies the health check endpoint returns 200 OK.
- Creates a new session and asserts a non-empty session ID is returned.
- Lists the sessions to confirm the newly created session exists.
- Sends a chat message (mocking the AI response) and asserts success.
- Retrieves the message history to verify both the user and AI messages are recorded.
- Generates a quiz with a mock topic and verifies that questions are returned.
- Submits a correct answer for the generated quiz item and validates the evaluation result is correct.

### 2. Negative / Edge Cases
These tests verify that our API gracefully handles incorrect user inputs or invalid states.
- **Session Not Found** (`test_session_not_found_404`): Requests message history for a non-existent session ID, expecting a 404 response.
- **Empty Content Message** (`test_empty_content_message_422`): Attempts to send a chat message containing only whitespace, verifying the API correctly returns a 422 Unprocessable Entity error.
- **Invalid ID Path Parameter** (`test_invalid_id_path_422`): Sends an invalid string (non-integer) as a `session_id` path parameter, expecting a 422 error due to FastAPI path parameter validation.
- **Quiz Item Not Found** (`test_submit_answer_not_found_404`): Submits an answer for a quiz item that does not exist in the database, verifying a 404 response is returned.


This file was written with AI assistance. All AI work was thoroughly checked by humans.