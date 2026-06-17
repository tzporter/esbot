## This file was written with AI assistance. All AI work was thoroughly checked by humans.

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from unittest.mock import patch
import sys
import os

# Add the backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app
from database import get_session

# Use an in-memory SQLite database for testing to ensure isolation
sqlite_url = "sqlite://"
engine = create_engine(
    sqlite_url, connect_args={"check_same_thread": False}, poolclass=StaticPool
)


def get_session_override():
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture():
    app.dependency_overrides[get_session] = get_session_override
    # Setup: Create tables before each test
    SQLModel.metadata.create_all(engine)
    with TestClient(app) as client:
        yield client
    # Teardown: Drop tables after each test
    SQLModel.metadata.drop_all(engine)
    app.dependency_overrides.clear()


def test_api_workflow_happy_path(client: TestClient):
    # 1. Health endpoint returns 200
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

    # 2. Creating a session
    response = client.post("/api/v1/sessions", json={"user_id": "test_user", "title": "Test Title"})
    assert response.status_code == 200
    session_data = response.json()
    assert "id" in session_data
    session_id = session_data["id"]
    assert session_id is not None

    # 3. Listing sessions for user
    response = client.get("/api/v1/sessions?user_id=test_user")
    assert response.status_code == 200
    sessions = response.json()
    assert len(sessions) == 1
    assert sessions[0]["id"] == session_id

    # Mock the AI provider before sending message and quiz
    with patch("main.ai_provider.get_explanation") as mock_explain, \
         patch("main.ai_provider.get_quiz") as mock_quiz, \
         patch("main.ai_provider.evaluate_answer") as mock_eval:
         
        mock_explain.return_value = "Mocked AI response"
        
        # 4. Sending a message
        response = client.post(
            f"/api/v1/sessions/{session_id}/messages", 
            json={"content": "Hello AI"}
        )
        assert response.status_code == 200
        assert "response" in response.json()
        assert response.json()["response"] == "Mocked AI response"

        # 5. Retrieve message history
        response = client.get(f"/api/v1/sessions/{session_id}/messages")
        assert response.status_code == 200
        messages = response.json()
        assert len(messages) >= 2 # User message + AI response
        assert any(m["content"] == "Hello AI" for m in messages)
        assert any(m["content"] == "Mocked AI response" for m in messages)

        # 6. Generate quiz
        mock_quiz.return_value = {
            "quiz": {
                "topic": "Python",
                "questions": [
                    {
                        "question": "What is Python?",
                        "answer": "A programming language."
                    }
                ]
            }
        }
        response = client.post(
            f"/api/v1/sessions/{session_id}/quiz", 
            json={"topic": "Python"}
        )
        assert response.status_code == 200
        quiz_data = response.json()
        assert "quiz" in quiz_data
        assert len(quiz_data["quiz"]["questions"]) == 1
        
        quiz_item_id = quiz_data["quiz"]["questions"][0]["id"]
        
        # 7. Submit correct answer
        mock_eval.return_value = {
            "is_correct": True,
            "feedback": "Good job!",
            "needs_clarification": False
        }
        response = client.post(
            f"/api/v1/quiz-items/{quiz_item_id}/submit",
            json={"user_answer": "A programming language."}
        )
        assert response.status_code == 200
        eval_data = response.json()
        assert eval_data["is_correct"] is True


def test_session_not_found_404(client: TestClient):
    response = client.get("/api/v1/sessions/9999/messages")
    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found"


def test_empty_content_message_422(client: TestClient):
    # Create session first
    response = client.post("/api/v1/sessions", json={"user_id": "test_user"})
    session_id = response.json()["id"]

    response = client.post(
        f"/api/v1/sessions/{session_id}/messages", 
        json={"content": "   "}
    )
    assert response.status_code == 422
    assert response.json()["detail"] == "Message cannot be empty"


def test_invalid_id_path_422(client: TestClient):
    # FastAPI path validation for integer session_id
    response = client.get("/api/v1/sessions/not_an_int/messages")
    assert response.status_code == 422


def test_submit_answer_not_found_404(client: TestClient):
    response = client.post(
        "/api/v1/quiz-items/9999/submit",
        json={"user_answer": "Does not matter"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Quiz item not found"
