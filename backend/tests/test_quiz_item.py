from pydantic import ValidationError
import pytest
from models import QuizItem, SubmittedAnswer, UserSession, QuizRequest


def test_quiz_item_creation():
    item = QuizItem(question_text="Capital of Germany?", correct_answer="Berlin", quiz_request_id=1)
    assert item.question_text == "Capital of Germany?"
    assert item.correct_answer == "Berlin"
    assert item.id is None


def test_no_answer_initially():
    item = QuizItem(question_text="Q?", correct_answer="A", quiz_request_id=1)
    assert item.submitted_answer is None


def test_empty_question_text_rejected():
    with pytest.raises(ValidationError):
        QuizItem.model_validate({"question_text": "", "correct_answer": "A", "quiz_request_id": 1})


def test_empty_correct_answer_rejected():
    with pytest.raises(ValidationError):
        QuizItem.model_validate({"question_text": "Q?", "correct_answer": "", "quiz_request_id": 1})


def test_missing_question_text_rejected():
    with pytest.raises(ValidationError):
        QuizItem.model_validate({"correct_answer": "A", "quiz_request_id": 1})


def test_missing_correct_answer_rejected():
    with pytest.raises(ValidationError):
        QuizItem.model_validate({"question_text": "Q?", "quiz_request_id": 1})


def test_item_links_to_quiz(db):
    s = UserSession()
    db.add(s)
    db.commit()
    db.refresh(s)

    qr = QuizRequest(topic="Geo", session_id=s.id)
    db.add(qr)
    db.commit()
    db.refresh(qr)

    item = QuizItem(question_text="Capital of France?", correct_answer="Paris", quiz_request_id=qr.id)
    db.add(item)
    db.commit()
    db.refresh(item)

    assert item.quiz_request.id == qr.id


def test_item_can_receive_answer(db):
    s = UserSession()
    db.add(s)
    db.commit()
    db.refresh(s)

    qr = QuizRequest(topic="Math", session_id=s.id)
    db.add(qr)
    db.commit()
    db.refresh(qr)

    item = QuizItem(question_text="2+2?", correct_answer="4", quiz_request_id=qr.id)
    db.add(item)
    db.commit()
    db.refresh(item)

    ans = SubmittedAnswer(user_answer="4", quiz_item_id=item.id)
    db.add(ans)
    db.commit()
    db.refresh(item)

    assert item.submitted_answer is not None
    assert item.submitted_answer.user_answer == "4"


def test_submit_helper(db):
    s = UserSession()
    db.add(s)
    db.commit()
    db.refresh(s)

    qr = QuizRequest(topic="Math", session_id=s.id)
    db.add(qr)
    db.commit()
    db.refresh(qr)

    item = QuizItem(question_text="3+3?", correct_answer="6", quiz_request_id=qr.id)
    db.add(item)
    db.commit()
    db.refresh(item)

    ans = item.submit("6")
    db.add(ans)
    db.commit()
    db.refresh(item)

    assert item.submitted_answer is not None
    assert item.submitted_answer.user_answer == "6"


def test_submit_helper_requires_persisted_item():
    item = QuizItem(question_text="Q?", correct_answer="A", quiz_request_id=1)
    with pytest.raises(ValueError, match="persisted"):
        item.submit("my answer")
