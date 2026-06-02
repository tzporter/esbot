from datetime import datetime, timedelta

import pytest
from sqlmodel import select

from models import UserSession, ChatMessage
from repositories.session_repository import SessionRepository


@pytest.fixture()
def repo(db):
    # A SessionRepository backed by the in-memory test database.
    return SessionRepository(db)


# create

def test_create_persists_session_and_assigns_id(repo, db):
    session = repo.create(user_id="alice")

    assert session.id is not None
    # Verify it is actually in the database, not just in memory.
    stored = db.get(UserSession, session.id)
    assert stored is not None
    assert stored.user_id == "alice"


def test_create_stores_optional_title(repo):
    session = repo.create(user_id="alice", title="Python basics")
    assert session.title == "Python basics"


def test_create_defaults_title_to_none(repo):
    session = repo.create(user_id="alice")
    assert session.title is None


# get_by_id

def test_get_by_id_returns_existing_session(repo):
    created = repo.create(user_id="alice")
    found = repo.get_by_id(created.id)
    assert found is not None
    assert found.id == created.id


def test_get_by_id_returns_none_for_unknown_id(repo):
    assert repo.get_by_id(9999) is None


# get_by_user

def test_get_by_user_returns_only_that_users_sessions(repo):
    repo.create(user_id="alice")
    repo.create(user_id="alice")
    repo.create(user_id="bob")

    alice_sessions = repo.get_by_user("alice")
    bob_sessions = repo.get_by_user("bob")

    assert len(alice_sessions) == 2
    assert len(bob_sessions) == 1
    assert all(s.user_id == "alice" for s in alice_sessions)


def test_get_by_user_returns_empty_list_for_unknown_user(repo):
    repo.create(user_id="alice")
    assert repo.get_by_user("nobody") == []


# append_message

def test_append_message_persists_message(repo, db):
    session = repo.create(user_id="alice")

    message = repo.append_message(session.id, content="hello", role="user")

    assert message.id is not None
    stored = db.get(ChatMessage, message.id)
    assert stored is not None
    assert stored.content == "hello"
    assert stored.role == "user"
    assert stored.session_id == session.id


def test_append_message_defaults_role_to_user(repo):
    session = repo.create(user_id="alice")
    message = repo.append_message(session.id, content="hi")
    assert message.role == "user"


def test_append_message_updates_last_activity(repo):
    session = repo.create(user_id="alice")

    # Persist a clearly old baseline so the comparison is unambiguous. We use a
    # committed value (not an in-memory tweak) to avoid SQLAlchemy's identity
    # map returning the same object for both reads.
    old_time = datetime(2000, 1, 1, 0, 0, 0)
    repo.update(session.id, last_activity=old_time)

    repo.append_message(session.id, content="hello")

    refreshed = repo.get_by_id(session.id)
    assert refreshed.last_activity > old_time


def test_append_message_to_unknown_session_raises(repo):
    with pytest.raises(ValueError, match="not found"):
        repo.append_message(9999, content="orphan")


# get_messages

def test_get_messages_returns_messages_in_chronological_order(repo):
    session = repo.create(user_id="alice")
    repo.append_message(session.id, content="first", role="user")
    repo.append_message(session.id, content="second", role="assistant")
    repo.append_message(session.id, content="third", role="user")

    messages = repo.get_messages(session.id)

    assert [m.content for m in messages] == ["first", "second", "third"]


def test_get_messages_returns_empty_list_when_no_messages(repo):
    session = repo.create(user_id="alice")
    assert repo.get_messages(session.id) == []


def test_get_messages_isolates_sessions(repo):
    s1 = repo.create(user_id="alice")
    s2 = repo.create(user_id="alice")
    repo.append_message(s1.id, content="only s1")

    assert len(repo.get_messages(s1.id)) == 1
    assert len(repo.get_messages(s2.id)) == 0


# update

def test_update_changes_title(repo):
    session = repo.create(user_id="alice", title="old")
    updated = repo.update(session.id, title="new")

    assert updated.title == "new"
    # Confirm the change was persisted, not just returned.
    assert repo.get_by_id(session.id).title == "new"


def test_update_changes_last_activity(repo):
    session = repo.create(user_id="alice")
    new_time = datetime(2030, 1, 1, 12, 0, 0)

    repo.update(session.id, last_activity=new_time)

    assert repo.get_by_id(session.id).last_activity == new_time


def test_update_leaves_unspecified_fields_untouched(repo):
    session = repo.create(user_id="alice", title="keep me")
    original_activity = session.last_activity

    repo.update(session.id, last_activity=original_activity + timedelta(days=1))

    refreshed = repo.get_by_id(session.id)
    assert refreshed.title == "keep me"  # title was not passed -> unchanged


def test_update_unknown_session_raises(repo):
    with pytest.raises(ValueError, match="not found"):
        repo.update(9999, title="ghost")


# delete

def test_delete_removes_session(repo):
    session = repo.create(user_id="alice")
    repo.delete(session.id)
    assert repo.get_by_id(session.id) is None


def test_delete_removes_associated_messages(repo, db):
    session = repo.create(user_id="alice")
    repo.append_message(session.id, content="msg1")
    repo.append_message(session.id, content="msg2")

    repo.delete(session.id)

    remaining = db.exec(
        select(ChatMessage).where(ChatMessage.session_id == session.id)
    ).all()
    assert remaining == []


def test_delete_unknown_session_is_noop(repo):
    # Should not raise even though the session does not exist.
    repo.delete(9999)


def test_delete_only_affects_target_session(repo):
    s1 = repo.create(user_id="alice")
    s2 = repo.create(user_id="alice")
    repo.append_message(s2.id, content="survivor")

    repo.delete(s1.id)

    assert repo.get_by_id(s2.id) is not None
    assert len(repo.get_messages(s2.id)) == 1
