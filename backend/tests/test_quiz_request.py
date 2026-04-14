from pydantic import ValidationError
import pytest
from models import QuizRequest, QuizItem, UserSession


def test_basic_creation():
    qr = QuizRequest(topic="Python", session_id=1)
    assert qr.topic == "Python"
    assert qr.id is None


def test_default_difficulty_is_medium():
    qr = QuizRequest(topic="Python", session_id=1)
    assert qr.difficulty == "medium"


def test_easy_and_hard_difficulty_accepted():
    easy = QuizRequest(topic="X", difficulty="easy", session_id=1)
    hard = QuizRequest(topic="X", difficulty="hard", session_id=1)
    assert easy.difficulty == "easy"
    assert hard.difficulty == "hard"


def test_invalid_difficulty_rejected():
    with pytest.raises(ValidationError):
        QuizRequest.model_validate({"topic": "X", "difficulty": "nightmare", "session_id": 1})


def test_empty_topic_rejected():
    with pytest.raises(ValidationError):
        QuizRequest.model_validate({"topic": "", "session_id": 1})


def test_missing_topic_rejected():
    with pytest.raises(ValidationError):
        QuizRequest.model_validate({"session_id": 1})


def test_missing_session_id_rejected():
    with pytest.raises(ValidationError):
        QuizRequest.model_validate({"topic": "Math"})


def test_quiz_belongs_to_session(db):
    s = UserSession()
    db.add(s)
    db.commit()
    db.refresh(s)

    qr = QuizRequest(topic="History", session_id=s.id)
    db.add(qr)
    db.commit()
    db.refresh(qr)

    assert qr.session.id == s.id


def test_quiz_collects_items(db):
    s = UserSession()
    db.add(s)
    db.commit()
    db.refresh(s)

    qr = QuizRequest(topic="Science", session_id=s.id)
    db.add(qr)
    db.commit()
    db.refresh(qr)

    db.add(QuizItem(question_text="What is H2O?", correct_answer="Water", quiz_request_id=qr.id))
    db.add(QuizItem(question_text="What is NaCl?", correct_answer="Salt", quiz_request_id=qr.id))
    db.commit()
    db.refresh(qr)

    assert len(qr.quiz_items) == 2


def test_session_lists_multiple_quizzes(db):
    s = UserSession()
    db.add(s)
    db.commit()
    db.refresh(s)

    for topic in ("Math", "History"):
        db.add(QuizRequest(topic=topic, session_id=s.id))
    db.commit()
    db.refresh(s)

    topics = {qr.topic for qr in s.quiz_requests}
    assert topics == {"Math", "History"}


def test_add_item_helper(db):
    s = UserSession()
    db.add(s)
    db.commit()
    db.refresh(s)

    qr = QuizRequest(topic="Geo", session_id=s.id)
    db.add(qr)
    db.commit()
    db.refresh(qr)

    item = qr.add_item("Capital of France?", "Paris")
    db.add(item)
    db.commit()
    db.refresh(qr)

    assert len(qr.quiz_items) == 1
    assert qr.quiz_items[0].question_text == "Capital of France?"


def test_add_item_helper_requires_persisted_request():
    qr = QuizRequest(topic="X", session_id=1)
    with pytest.raises(ValueError, match="persisted"):
        qr.add_item("Q?", "A")
