from datetime import datetime, timedelta
import pytest
from models import UserSession, ChatMessage, QuizRequest


def test_new_session_has_no_id():
    s = UserSession()
    assert s.id is None


def test_created_at_is_set_automatically():
    before = datetime.utcnow()
    s = UserSession()
    after = datetime.utcnow()
    assert isinstance(s.created_at, datetime)
    assert before - timedelta(seconds=1) <= s.created_at <= after + timedelta(seconds=1)


def test_empty_lists_by_default():
    s = UserSession()
    assert s.messages == []
    assert s.quiz_requests == []


def test_session_persists_and_gets_id(db):
    s = UserSession()
    db.add(s)
    db.commit()
    db.refresh(s)
    assert s.id is not None


def test_add_messages_to_session(db):
    s = UserSession()
    db.add(s)
    db.commit()
    db.refresh(s)

    db.add(ChatMessage(content="hello", role="user", session_id=s.id))
    db.add(ChatMessage(content="hey", role="assistant", session_id=s.id))
    db.commit()
    db.refresh(s)

    assert len(s.messages) == 2
    contents = {m.content for m in s.messages}
    assert "hello" in contents
    assert "hey" in contents


def test_add_quiz_request_to_session(db):
    s = UserSession()
    db.add(s)
    db.commit()
    db.refresh(s)

    db.add(QuizRequest(topic="Python", session_id=s.id))
    db.commit()
    db.refresh(s)

    assert len(s.quiz_requests) == 1
    assert s.quiz_requests[0].topic == "Python"


def test_sessions_dont_share_messages(db):
    s1 = UserSession()
    s2 = UserSession()
    db.add_all([s1, s2])
    db.commit()
    db.refresh(s1)
    db.refresh(s2)

    db.add(ChatMessage(content="only s1", role="user", session_id=s1.id))
    db.commit()
    db.refresh(s1)
    db.refresh(s2)

    assert len(s1.messages) == 1
    assert len(s2.messages) == 0


def test_add_message_helper(db):
    s = UserSession()
    db.add(s)
    db.commit()
    db.refresh(s)

    msg = s.add_message("hello from helper")
    db.add(msg)
    db.commit()
    db.refresh(s)

    assert len(s.messages) == 1
    assert s.messages[0].content == "hello from helper"
    assert s.messages[0].role == "user"


def test_add_message_helper_with_role(db):
    s = UserSession()
    db.add(s)
    db.commit()
    db.refresh(s)

    msg = s.add_message("bot reply", role="assistant")
    db.add(msg)
    db.commit()
    db.refresh(s)

    assert s.messages[0].role == "assistant"


def test_add_message_helper_requires_persisted_session():
    s = UserSession()
    with pytest.raises(ValueError, match="persisted"):
        s.add_message("too early")


def test_add_quiz_request_helper(db):
    s = UserSession()
    db.add(s)
    db.commit()
    db.refresh(s)

    qr = s.add_quiz_request("History", difficulty="hard")
    db.add(qr)
    db.commit()
    db.refresh(s)

    assert len(s.quiz_requests) == 1
    assert s.quiz_requests[0].topic == "History"
    assert s.quiz_requests[0].difficulty == "hard"


def test_add_quiz_request_helper_requires_persisted_session():
    s = UserSession()
    with pytest.raises(ValueError, match="persisted"):
        s.add_quiz_request("Math")
