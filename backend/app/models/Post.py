from datetime import datetime
from app.db import Base, get_db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, select, func
from sqlalchemy.orm import relationship, column_property
from .User import User
from .Like import Like

db = get_db()

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(String(350), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    like_count = column_property(
        select([func.count(Like.id)]).where(Like.post_id == id)
    )
    
    user = relationship('User') # , foreign_keys=user_id
    comments = relationship('Comment', cascade='all,delete')
    likes = relationship('Like', cascade='all,delete')
    
    def getPosts():
        posts = db.query(Post).all()
        return [{
            "id": i.id,
            "title": i.title,
            "content": i.content,
            "user": getUser(i.user_id)
        } for i in posts]
    
    def getUserPosts(uid):
        posts = db.query(Post).filter(Post.user_id == uid).all()
        return [{"id": i.id, "user_id": i.user_id, "title": i.title, "content": i.content} for i in posts]
    
    def createPost(title, content, uid):
        if (title and content and uid):
            try:
                user = list(filter(lambda i: i.id == uid, db.query(User).all()))[0]
                post = Post(
                    title = title,
                    content = content,
                    user = user
                )
                db.add(post)
                db.commit()
            except Exception as e:
                print(e)
                return False
        else:
            return False
    
    def deletePost(pid):
        if(pid):
            try:
                post = db.query(Post).get(pid)
                db.delete(post)
                db.commit()
                return True
            except Exception as e:
                print (e)
                return False