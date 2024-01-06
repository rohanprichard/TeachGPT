from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Text,
    Boolean,
)
from typing import List
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"
    name = Column(String)
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    department = Column(String)
    year = Column(String)
    subjects = Column(List[String])
    chats = relationship("Chat", back_populates="user")


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime, index=True)
    description = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    messages = relationship(
        "ChatMessage", back_populates="chat"
    )
    user = relationship("User", back_populates="chats")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String(128), primary_key=True)
    created_at = Column(DateTime)
    chat_id = Column(String(128), ForeignKey(column="chat.id"))
    chat = relationship("Chat", back_populates="messages")
    message = Column(Text())
    from_user = Column(Boolean())
    is_opener = Column(Boolean(), default=False)
