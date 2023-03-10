from app.db import get_db
from app.models import User, Post, Comment

def get_user(uid):
    db = get_db()
    user = db.query(User).filter(User.id == uid).one()
    return {"id": user.id, "username": user.username, "email": user.email}

def get_user_posts(uid):
    db = get_db()
    posts = db.query(Post).filter(Post.user_id == uid).order_by(Post.created_at.desc())
    return [{"id": i.id, "title": i.title, "content": i.content, 'created_at': i.created_at, 'updated_at': i.updated_at, 'like_count': i.like_count, 'comments': i.comments, 'likes': i.likes} for i in posts]

def get_comments(pid):
    db = get_db()
    comments = db.query(Comment).filter(Comment.post_id==pid).order_by(Comment.created_at.desc())
    return [{"id": i.id, "comment_text": i.comment_text, "user_id": i.user_id, 'user': get_user(i.user_id), 'created_at': i.created_at, 'updated_at': i.updated_at} for i in comments]
