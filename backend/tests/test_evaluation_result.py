from pydantic import ValidationError
import pytest
from models import EvaluationResult, SubmittedAnswer, UserSession, QuizRequest, QuizItem


def test_correct_result():
    ev = EvaluationResult(is_correct=True, feedback="Well done", submitted_answer_id=1)
    assert ev.is_correct is True
    assert ev.feedback == "Well done"


def test_incorrect_result():
    ev = EvaluationResult(is_correct=False, feedback="Try again", submitted_answer_id=1)
    assert ev.is_correct is False


def test_missing_is_correct_rejected():
    with pytest.raises(ValidationError):
        EvaluationResult.model_validate({"feedback": "hmm", "submitted_answer_id": 1})


def test_missing_feedback_rejected():
    with pytest.raises(ValidationError):
        EvaluationResult.model_validate({"is_correct": True, "submitted_answer_id": 1})


def test_empty_feedback_rejected():
    with pytest.raises(ValidationError):
        EvaluationResult.model_validate({"is_correct": True, "feedback": "", "submitted_answer_id": 1})


def test_missing_submitted_answer_id_rejected():
    with pytest.raises(ValidationError):
        EvaluationResult.model_validate({"is_correct": True, "feedback": "ok"})


def test_eval_links_back_to_answer(db):
    s = UserSession()
    db.add(s)
    db.commit()
    db.refresh(s)

    qr = QuizRequest(topic="Bio", session_id=s.id)
    db.add(qr)
    db.commit()
    db.refresh(qr)

    item = QuizItem(question_text="DNA stands for?", correct_answer="Deoxyribonucleic acid", quiz_request_id=qr.id)
    db.add(item)
    db.commit()
    db.refresh(item)

    ans = SubmittedAnswer(user_answer="Deoxyribonucleic acid", quiz_item_id=item.id)
    db.add(ans)
    db.commit()
    db.refresh(ans)

    ev = EvaluationResult(is_correct=True, feedback="Exactly right", submitted_answer_id=ans.id)
    db.add(ev)
    db.commit()
    db.refresh(ev)
    db.refresh(ans)

    assert ev.submitted_answer.id == ans.id
    assert ans.evaluation.id == ev.id
