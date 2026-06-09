# This file was generated with AI assistance. All code was thoroughly checked by humans.

import pytest
import sys
import os
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

# Add the backend directory to sys.path so we can import main and database
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from unittest.mock import patch

from main import app
from database import get_session

# Setup in-memory sqlite database for testing
sqlite_url = "sqlite://"
engine = create_engine(
    sqlite_url, connect_args={"check_same_thread": False}, poolclass=StaticPool
)


def get_session_override():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_session] = get_session_override


@pytest.fixture(name="client")
def client_fixture():
    # Create the db tables for testing
    SQLModel.metadata.create_all(engine)
    with TestClient(app) as client:
        yield client
    # Clean up after tests
    SQLModel.metadata.drop_all(engine)


def test_create_and_list_sessions(client: TestClient):
    # Test creating a session
    response = client.post(
        "/sessions", json={"user_id": "anonymous", "title": "Test Session"}
    )
    assert response.status_code == 200
    session_data = response.json()
    assert session_data["title"] == "Test Session"
    session_id = session_data["id"]

    # Test listing sessions
    response = client.get("/sessions")
    assert response.status_code == 200
    sessions = response.json()
    assert len(sessions) == 1
    assert sessions[0]["id"] == session_id


@patch("main.ai_provider.get_explanation")
def test_chat_messages(mock_get_explanation, client: TestClient):
    mock_get_explanation.return_value = "hello, user!"
    # Create a session first
    response = client.post("/sessions", json={"user_id": "anonymous"})
    session_id = response.json()["id"]

    # Post a message
    response = client.post(
        f"/sessions/{session_id}/messages", json={"content": "Hi there!"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data

    # Retrieve messages
    response = client.get(f"/sessions/{session_id}/messages")
    assert response.status_code == 200
    messages = response.json()
    assert len(messages) == 2  # 1 user message + 1 assistant message
    assert messages[0]["content"] == "Hi there!"
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"


def test_delete_session(client: TestClient):
    # Create a session
    response = client.post("/sessions", json={"user_id": "anonymous"})
    session_id = response.json()["id"]

    # Delete the session
    response = client.delete(f"/sessions/{session_id}")
    assert response.status_code == 200

    # Verify it's deleted
    response = client.get("/sessions")
    assert len(response.json()) == 0
