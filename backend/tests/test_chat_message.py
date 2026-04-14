from pydantic import ValidationError
import pytest
from models import ChatMessage, UserSession


def test_valid_message():
    msg = ChatMessage(content="hello", role="user", session_id=1)
    assert msg.content == "hello"
    assert msg.role == "user"
    assert msg.id is None


def test_default_role_is_user():
    msg = ChatMessage(content="test", session_id=1)
    assert msg.role == "user"


def test_assistant_role_works():
    msg = ChatMessage(content="hi back", role="assistant", session_id=1)
    assert msg.role == "assistant"


def test_system_role_works():
    msg = ChatMessage(content="system prompt", role="system", session_id=1)
    assert msg.role == "system"


def test_empty_content_fails():
    with pytest.raises(ValidationError):
        ChatMessage.model_validate({"content": "", "session_id": 1})


def test_missing_content_fails():
    with pytest.raises(ValidationError):
        ChatMessage.model_validate({"role": "user", "session_id": 1})


def test_missing_session_id_fails():
    with pytest.raises(ValidationError):
        ChatMessage.model_validate({"content": "hi", "role": "user"})


def test_invalid_role_rejected():
    with pytest.raises(ValidationError):
        ChatMessage.model_validate({"content": "hi", "role": "moderator", "session_id": 1})


def test_message_belongs_to_session(db):
    s = UserSession()
    db.add(s)
    db.commit()
    db.refresh(s)

    msg = ChatMessage(content="hey", role="user", session_id=s.id)
    db.add(msg)
    db.commit()
    db.refresh(msg)

    assert msg.session.id == s.id


def test_session_sees_its_messages(db):
    s = UserSession()
    db.add(s)
    db.commit()
    db.refresh(s)

    db.add(ChatMessage(content="ping", role="user", session_id=s.id))
    db.commit()
    db.refresh(s)

    assert len(s.messages) == 1
    assert s.messages[0].content == "ping"
