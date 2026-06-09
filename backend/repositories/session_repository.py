from datetime import datetime
from typing import List, Optional

from sqlmodel import Session, select

from models import UserSession, ChatMessage


# Data-access layer for UserSession and its ChatMessages.
#
# All database interaction for sessions is encapsulated here so that the
# business-logic layer (e.g. ChatService) never has to touch the ORM
# directly. The repository receives an open database Session via its
# constructor (dependency injection) and reuses it for every operation.
class SessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: str, title: Optional[str] = None) -> UserSession:
        # Persist a new learning session and return it with its assigned id.
        session = UserSession(user_id=user_id, title=title)
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_by_id(self, session_id: int) -> Optional[UserSession]:
        # Return the session with the given id, or None if it does not exist.
        return self.db.get(UserSession, session_id)

    def get_by_user(self, user_id: str) -> List[UserSession]:
        # Return all sessions belonging to a given user.
        statement = select(UserSession).where(UserSession.user_id == user_id)
        return list(self.db.exec(statement).all())

    def append_message(
        self, session_id: int, content: str, role: str = "user"
    ) -> ChatMessage:
        # Store a new message linked to an existing session.
        #
        # Raises ValueError if the session does not exist. Touches the session's
        # last_activity timestamp so metadata stays consistent.
        session = self.db.get(UserSession, session_id)
        if session is None:
            raise ValueError(f"Session {session_id} not found")

        message = ChatMessage(content=content, role=role, session_id=session_id)
        self.db.add(message)

        session.last_activity = datetime.utcnow()
        self.db.add(session)

        self.db.commit()
        self.db.refresh(message)
        return message

    def get_messages(self, session_id: int) -> List[ChatMessage]:
        # Return all messages of a session in chronological order (oldest first).
        statement = (
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.id)
        )
        return list(self.db.exec(statement).all())

    def update(
        self,
        session_id: int,
        title: Optional[str] = None,
        last_activity: Optional[datetime] = None,
    ) -> UserSession:
        # Update mutable session metadata (title and/or last_activity).
        #
        # Only the arguments that are explicitly provided are changed; passing
        # nothing but the id leaves the session untouched. Raises ValueError if
        # the session does not exist.
        session = self.db.get(UserSession, session_id)
        if session is None:
            raise ValueError(f"Session {session_id} not found")

        if title is not None:
            session.title = title
        if last_activity is not None:
            session.last_activity = last_activity

        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def delete(self, session_id: int) -> None:
        # Remove a session together with all of its messages.
        #
        # Messages are deleted explicitly first so the operation does not rely on
        # database-level cascade configuration. Silently does nothing if the
        # session does not exist.
        session = self.db.get(UserSession, session_id)
        if session is None:
            return

        messages = self.db.exec(
            select(ChatMessage).where(ChatMessage.session_id == session_id)
        ).all()
        for message in messages:
            self.db.delete(message)

        self.db.delete(session)
        self.db.commit()
