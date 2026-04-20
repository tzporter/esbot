from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator
from typing import List, Optional
from datetime import datetime


class UserSession(SQLModel, table=True):
    """Represents a user session, which can have multiple chat messages and quiz requests associated with it."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    messages: List["ChatMessage"] = Relationship(back_populates="session")
    quiz_requests: List["QuizRequest"] = Relationship(back_populates="session")

    def add_message(self, content: str, role: str = "user") -> "ChatMessage":
        if self.id is None:
            raise ValueError("Session must be persisted before adding messages")
        msg = ChatMessage(content=content, role=role, session_id=self.id)
        self.messages.append(msg)
        return msg

    def add_quiz_request(self, topic: str, difficulty: str = "medium") -> "QuizRequest":
        if self.id is None:
            raise ValueError("Session must be persisted before adding quiz requests")
        qr = QuizRequest(topic=topic, difficulty=difficulty, session_id=self.id)
        self.quiz_requests.append(qr)
        return qr


class ChatMessage(SQLModel, table=True):
    """Represents a chat message associated with a user session."""
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str = Field(nullable=False, min_length=1)
    role: str = Field(default="user")

    session_id: int = Field(foreign_key="usersession.id")
    session: UserSession = Relationship(back_populates="messages")

    @field_validator("role")
    @classmethod
    def check_role(cls, v):
        allowed = ("user", "assistant", "system")
        if v not in allowed:
            raise ValueError(f"role must be one of {allowed}")
        return v


class QuizRequest(SQLModel, table=True):
    """Represents a quiz request associated with a user session."""
    id: Optional[int] = Field(default=None, primary_key=True)
    topic: str = Field(nullable=False, min_length=1)
    difficulty: str = Field(default="medium")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("difficulty")
    @classmethod
    def check_difficulty(cls, v):
        allowed = ("easy", "medium", "hard")
        if v not in allowed:
            raise ValueError(f"difficulty must be one of {allowed}")
        return v

    session_id: int = Field(foreign_key="usersession.id")
    session: UserSession = Relationship(back_populates="quiz_requests")

    quiz_items: List["QuizItem"] = Relationship(back_populates="quiz_request")

    def add_item(self, question_text: str, correct_answer: str) -> "QuizItem":
        if self.id is None:
            raise ValueError("QuizRequest must be persisted before adding items")
        item = QuizItem(
            question_text=question_text,
            correct_answer=correct_answer,
            quiz_request_id=self.id,
        )
        self.quiz_items.append(item)
        return item


class QuizItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question_text: str = Field(nullable=False, min_length=1)
    correct_answer: str = Field(nullable=False, min_length=1)

    quiz_request_id: int = Field(foreign_key="quizrequest.id")
    quiz_request: QuizRequest = Relationship(back_populates="quiz_items")

    submitted_answer: Optional["SubmittedAnswer"] = Relationship(back_populates="quiz_item")

    def submit(self, user_answer: str) -> "SubmittedAnswer":
        if self.id is None:
            raise ValueError("QuizItem must be persisted before submitting an answer")
        ans = SubmittedAnswer(user_answer=user_answer, quiz_item_id=self.id)
        self.submitted_answer = ans
        return ans


class SubmittedAnswer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_answer: str = Field(nullable=False, min_length=1)

    quiz_item_id: int = Field(foreign_key="quizitem.id")
    quiz_item: QuizItem = Relationship(back_populates="submitted_answer")

    evaluation: Optional["EvaluationResult"] = Relationship(back_populates="submitted_answer")

    def evaluate(self, is_correct: bool, feedback: str) -> "EvaluationResult":
        if self.id is None:
            raise ValueError("SubmittedAnswer must be persisted before evaluating")
        ev = EvaluationResult(
            is_correct=is_correct,
            feedback=feedback,
            submitted_answer_id=self.id,
        )
        self.evaluation = ev
        return ev


class EvaluationResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    is_correct: bool = Field(nullable=False)
    feedback: str = Field(nullable=False, min_length=1)

    submitted_answer_id: int = Field(foreign_key="submittedanswer.id")
    submitted_answer: SubmittedAnswer = Relationship(back_populates="evaluation")
