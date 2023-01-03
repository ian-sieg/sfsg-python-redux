from app.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Like(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(100), ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))