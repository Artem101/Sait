from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,Text
from sqlalchemy.orm import declarative_base, relationship, object_session

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    password = Column(Text)
    num_posts = Column(Integer, default=0)
    code = Column(Integer, default=0)
    registration_time = Column(DateTime, default=datetime.now)
    deleted_at = Column(DateTime, default=None, onupdate=datetime.now)

    def __init__(self, code):
        self.code = code
        self.registration_time = datetime.now()

    def delete_after_time(self):
        session = object_session(self)
        session.expire(self)
        session.refresh(self)
        self.deleted_at = datetime.utcnow() + timedelta(minutes=10)
        session.add(self)
        session.commit()

        # проверяем, прошло ли 10 минут с момента создания записи
        if self.deleted_at is not None and self.deleted_at < datetime.utcnow():
            self.code = 0
            session.add(self)
            session.commit()




class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    description = Column(Text)
    content = Column(Text)
    post_creator_name = Column(Text)
    views = Column(Integer, default=0)
    like = Column(Integer, default=0)
    registration_time = Column(DateTime, default=datetime.now)

class Like(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User")
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship("Post")

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    text = Column(Text)
    author = Column(Text)
    date = Column(DateTime, default=datetime.now)

class ChatGtp(Base):
    __tablename__ = 'chatgpt'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    message_text = Column(Text)
    query = Column(Text)
    datetime = Column(DateTime, default=datetime.now)



