import pytest
import sys
import os
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

# Add the backend directory to sys.path so we can import main and database
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

def test_chat_and_history(client: TestClient):
    # Test posting a message
    response = client.post("/chat", json={"content": "Hi there!"})
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "assistant"
    assert data["content"] == "hello, user!"
    
    # Test retrieving history
    response = client.get("/history")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # 1 user message + 1 assistant message
    assert data[0]["content"] == "Hi there!"
    assert data[0]["role"] == "user"
    assert data[1]["content"] == "hello, user!"
    assert data[1]["role"] == "assistant"
