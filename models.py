from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from forum import Base

import time
from werkzeug.security import generate_password_hash, check_password_hash
import os
from _md5 import md5

secret_key = "jia135AcF1å122S12!asdf89u89135DSAFkOi!j"

class Thread(Base):
    __tablename__ = 'threads'
    title = Column(String, unique=True)
    threadId = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    userId = Column(String)
    date = Column(Integer, nullable=False)
    content = Column(String, nullable=False)

    def __init__(self, title, threadId, content):
        self.title = title
        self.threadId = threadId
        self.content = content
        self.date = int(time.time())
        
    def __repr__(self):
        return '<Thread %r>' % (self.title)

class User(Base):
    __tablename__ = 'users'
    userId = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String, nullable=False, unique=True)
    salt = Column(String, unique=True)
    pw_hash = Column(String, unique=True)
    threads = Column(Integer)
    comments = relationship("Comment")

    def __init__(self, name, password, threads=None):
        self.name = name
        self.threads = threads
        self.set_password(password)

    def set_password(self, password):
        self.salt = str(os.urandom(8))
        self.pw_hash = generate_password_hash(password + self.salt + secret_key)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password + self.salt + secret_key)

    def __repr__(self):
        return '<User %r>' % (self.name)

class Comment(Base):
    __tablename__ = 'comments'
    commentId = Column(Integer, nullable=False, primary_key=True, unique=True, autoincrement=True)
    threadId = Column(Integer, nullable=False)
    text = Column(String)
    userId = Column(Integer, ForeignKey('users.userId'))
    user = relationship("User", backref=backref('users', uselist=True, cascade='delete,all'))

    def __init__(self, userId, threadId, text=None):
        self.userId = userId
        self.threadId = threadId
        self.text = text

    def __repr__(self):
        return '<Comment %r>' % (self.text)

"""class Password(Base):
    __tablename__ = 'passwords'
    password = Column(String, nullable=False)
    userId = Column(Integer, ForeignKey('users.userId'))
    user = relationship("User", backref=backref('users', uselist=True, cascade='delete,all'))

    def __init__(self, password, userId):
        self.password = password
        self.userId = userId"""