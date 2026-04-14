from pydantic import ValidationError
import pytest
from models import SubmittedAnswer, EvaluationResult, UserSession, QuizRequest, QuizItem


def test_answer_creation():
    ans = SubmittedAnswer(user_answer="42", quiz_item_id=1)
    assert ans.user_answer == "42"
    assert ans.evaluation is None


def test_empty_answer_rejected():
    with pytest.raises(ValidationError):
        SubmittedAnswer.model_validate({"user_answer": "", "quiz_item_id": 1})


def test_missing_answer_rejected():
    with pytest.raises(ValidationError):
        SubmittedAnswer.model_validate({"quiz_item_id": 1})


def test_missing_quiz_item_id_rejected():
    with pytest.raises(ValidationError):
        SubmittedAnswer.model_validate({"user_answer": "something"})


def _make_item(db):
    s = UserSession()
    db.add(s)
    db.commit()
    db.refresh(s)

    qr = QuizRequest(topic="Trivia", session_id=s.id)
    db.add(qr)
    db.commit()
    db.refresh(qr)

    item = QuizItem(question_text="Largest planet?", correct_answer="Jupiter", quiz_request_id=qr.id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def test_answer_belongs_to_item(db):
    item = _make_item(db)

    ans = SubmittedAnswer(user_answer="Jupiter", quiz_item_id=item.id)
    db.add(ans)
    db.commit()
    db.refresh(ans)

    assert ans.quiz_item.id == item.id


def test_full_chain_item_to_answer_to_eval(db):
    item = _make_item(db)

    ans = SubmittedAnswer(user_answer="Jupiter", quiz_item_id=item.id)
    db.add(ans)
    db.commit()
    db.refresh(ans)

    ev = EvaluationResult(is_correct=True, feedback="Correct!", submitted_answer_id=ans.id)
    db.add(ev)
    db.commit()
    db.refresh(ans)

    assert ans.evaluation.is_correct is True
    assert ans.evaluation.feedback == "Correct!"

    db.refresh(item)
    assert item.submitted_answer.id == ans.id


def test_evaluate_helper(db):
    item = _make_item(db)

    ans = SubmittedAnswer(user_answer="Jupiter", quiz_item_id=item.id)
    db.add(ans)
    db.commit()
    db.refresh(ans)

    ev = ans.evaluate(is_correct=True, feedback="Well done")
    db.add(ev)
    db.commit()
    db.refresh(ans)

    assert ans.evaluation is not None
    assert ans.evaluation.is_correct is True
    assert ans.evaluation.feedback == "Well done"


def test_evaluate_helper_requires_persisted_answer():
    ans = SubmittedAnswer(user_answer="guess", quiz_item_id=1)
    with pytest.raises(ValueError, match="persisted"):
        ans.evaluate(True, "feedback")
