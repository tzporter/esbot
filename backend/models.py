from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime


class UserSession(SQLModel, table=True):
    """Represents a single chat session to organize conversation history."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # One session can have many messages and many quiz requests
    messages: List["ChatMessage"] = Relationship(back_populates="session")
    quiz_requests: List["QuizRequest"] = Relationship(back_populates="session")

class ChatMessage(SQLModel, table=True):
    """Stores individual messages within a session."""
    id: Optional[int] = Field(default=None, primary_key=True)
    # Content can not be blank
    content: str = Field(nullable=False, min_length=1) 
    role: str = Field(default="user")
    
    # Foreign key to link to UserSession
    session_id: int = Field(foreign_key="usersession.id")
    session: UserSession = Relationship(back_populates="messages")


class QuizRequest(SQLModel, table=True):
    """The request generated when a user asks for a quiz on a topic."""
    id: Optional[int] = Field(default=None, primary_key=True)
    topic: str = Field(nullable=False, min_length=1) # Validation requirement
    difficulty: str = Field(default="medium")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Links back to the session
    session_id: int = Field(foreign_key="usersession.id")
    session: UserSession = Relationship(back_populates="quiz_requests")
    
    # One request generates many quiz items 
    quiz_items: List["QuizItem"] = Relationship(back_populates="quiz_request")

class QuizItem(SQLModel, table=True):
    """An individual question generated as part of a QuizRequest."""
    id: Optional[int] = Field(default=None, primary_key=True)
    question_text: str = Field(nullable=False)
    correct_answer: str = Field(nullable=False)
    
    # Foreign key to the specific request
    quiz_request_id: int = Field(foreign_key="quizrequest.id")
    quiz_request: QuizRequest = Relationship(back_populates="quiz_items")
    
    # One question has one submitted answer
    submitted_answer: Optional["SubmittedAnswer"] = Relationship(back_populates="quiz_item")

class SubmittedAnswer(SQLModel, table=True):
    """The user's response to a specific QuizItem."""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_answer: str = Field(nullable=False)
    
    # Link to the specific question
    quiz_item_id: int = Field(foreign_key="quizitem.id")
    quiz_item: QuizItem = Relationship(back_populates="submitted_answer")
    
    # Link to the AI's feedback
    evaluation: Optional["EvaluationResult"] = Relationship(back_populates="submitted_answer")

class EvaluationResult(SQLModel, table=True):
    """The AI feedback provided after evaluating a user's answer."""
    id: Optional[int] = Field(default=None, primary_key=True)
    is_correct: bool = Field(nullable=False)
    feedback: str = Field(nullable=False) # The explanation provided by the AI
    
    # Link to the submitted answer
    submitted_answer_id: int = Field(foreign_key="submittedanswer.id")
    submitted_answer: SubmittedAnswer = Relationship(back_populates="evaluation")