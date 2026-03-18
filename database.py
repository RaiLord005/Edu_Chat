import os
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(4), unique=True, index=True)  # 4-digit random ID
    username = Column(String(50), unique=True, index=True)
    password = Column(String(255))  # Will be hashed
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Textbook(Base):
    __tablename__ = "books" 
    id = Column(Integer, primary_key=True, index=True)
    class_level = Column("class", Integer) 
    book = Column(String(255))
    filepath = Column(String(255))

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(4), ForeignKey("users.user_id", ondelete="CASCADE"), index=True)
    title = Column(String(255))
    class_level = Column(Integer)
    subject = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id", ondelete="CASCADE"))
    sender = Column(String(50)) # 'user' or 'bot'
    message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())