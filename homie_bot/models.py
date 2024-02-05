from sqlalchemy import Column, String, Integer, DateTime, Text, Index
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserInfo(Base):
    __tablename__ = 'user_info'
    username = Column(String(), primary_key=True)
    server = Column(String(), primary_key=True)
    backstory = Column(String(), nullable=True)


class Message(Base):
    __tablename__ = 'messages'
    message_id = Column(Integer, primary_key=True)
    server = Column(String(), primary_key=True)
    channel = Column(String(), primary_key=True)

    username = Column(String(), nullable=False)
    timestamp = Column(DateTime(), nullable=False)
    content = Column(Text(), nullable=False)


recent_messages_index = Index(
    'recent_messages_index', Message.server, Message.channel, Message.timestamp
)
recent_user_messages_index = Index(
    'recent_user_messages_index', Message.server, Message.channel, Message.username,
    Message.timestamp
)


class Lore(Base):
    __tablename__ = 'lore'

    server = Column(String(), primary_key=True)
    channel = Column(String(), primary_key=True)

    names = Column(String())
    content = Column(Text())
