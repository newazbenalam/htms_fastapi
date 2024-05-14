from sqlalchemy import Boolean, DateTime, Engine, ForeignKey, Integer, Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True, index=True)
  username= Column(String(64), unique=True)
  created_at = Column(DateTime(timezone=True), server_default=func.now())
  updated_at = Column(DateTime(timezone=True), onupdate=func.now(), default=func.now(),server_default=func.now())
  post = relationship('Post', backref='users')
  
class Post(Base):
  __tablename__ = 'posts'
  id = Column(Integer, primary_key=True, index=True)
  title = Column(String(64))
  content = Column(String(255))
  created_at = Column(DateTime(timezone=True), server_default=func.now())
  updated_at = Column(DateTime(timezone=True), onupdate=func.now())
  user_id = Column(Integer, ForeignKey('users.id'))
  
  
  
  