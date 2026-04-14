import sys, os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from models import (
    UserSession, ChatMessage, QuizRequest,
    QuizItem, SubmittedAnswer, EvaluationResult,
)

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@pytest.fixture(autouse=True)
def setup_db():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


@pytest.fixture()
def db():
    with Session(engine) as session:
        yield session
