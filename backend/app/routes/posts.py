from flask import Blueprint, request, jsonify, make_response, session
from app.models import User, Post, Comment, Like
from app.db import get_db
from datetime import datetime, timedelta
from app.utils.helpers import get_user, get_comments
from app.utils.auth import login_required

bp = Blueprint('posts', __name__, url_prefix='/api/posts')


@bp.route('/', methods = ['GET'])
def get_posts():
    db = get_db()
    posts = db.query(Post).all()
    return [{
            "id": i.id,
            "title": i.title,
            "content": i.content,
            "user_id": i.user_id,
            'user': get_user(i.user_id),
            'comments': get_comments(i.id),
            'like_count': i.like_count,
            'created_at': i.created_at,
            'updated_at': i.updated_at
    } for i in posts]

@bp.route('/new', methods=['POST'])
def new_post():
    data = request.get_json()
    db = get_db()

    title = data['title']
    content = data['content']
    user_id = session.get('user_id')
    
    if title and content and user_id:
        try:
            user = list(filter(lambda i: i.id == user_id, db.query(User).all()))[0]
            post = Post(
                title=title,
                content=content,
                user=user
            )
            db.add(post)
            db.commit()
            return jsonify({'success': 'true'})
        except Exception as e:
            print(e)
            return jsonify({'error': 'Invalid form'})
    else:
        return jsonify({'error': 'Please include both a title and content'})

@bp.route('/<id>', methods=['PUT', 'DELETE'])
@login_required
def posts(id):
    method = request.method
    db = get_db()
    
    if (method == 'DELETE'):
        try:
            post = db.query(Post).filter(Post.id == id).one()
            if post.user_id == session.get('user_id'):
                db.delete(post)
                db.commit()
                return jsonify({'success': True})
            else:
                return jsonify({'message':'Wrong user'})
        except Exception as e:
            print (e)
            return jsonify({'error': False})
    
    elif(method == 'PUT'):
        try:
            post = db.query(Post).filter(Post.id == id).one()
            if post:
                data = request.get_json()
                title = data['title']
                content = data['content']
                user_id = session.get('user_id')

                post.title = title
                post.content = content
                post.user_id = user_id
                db.commit()
                return jsonify({'success': 'true'})
            else:
                return jsonify({'error': 'No post with this id'})
        except Exception as e:
            print(e)
            return jsonify({'error': 'Invalid form'})

@bp.route('/<id>/comments', methods=['POST', 'PUT', 'DELETE'])
@login_required
def comment(id):
    method = request.method
    data = request.get_json()
    db = get_db()
    if method == 'POST':
        try:
            newComment = Comment(
                comment_text = data['comment_text'],
                post_id=id,
                user_id=session.get('user_id')
            )
            db.add(newComment)
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()
            return jsonify(message ='Comment failed to post')

        return jsonify(id=newComment.id)
    
    elif method == 'PUT':
        #TODO: make sure to hide comment id in frontend edit button to send along to backend
        try:
            id = data['id']
            comment_text = data['comment_text']
            comment = db.query(Comment).filter(Comment.id == id).one()
            
            if comment.user_id == session.get('user_id'):
                comment.comment_text = comment_text
                db.commit()
                return jsonify({'message': 'Comment posted!'})
            else:
                return jsonify({'error': 'Wrong user'})
        except Exception as e:
            print(e)
            db.rollback()
            return jsonify(message ='Comment failed to post')
    
    elif method == 'DELETE':
        #TODO: make sure to hide comment id in frontend edit button to send along to backend
        try:
            id = data['id']
            comment = db.query(Comment).filter(Comment.id == id).one()
            
            if comment.user_id == session.get('user_id'):
                db.delete(comment)
                db.commit()
                return jsonify({'success': True})
            else:
                return jsonify({'error': 'Wrong user'})
        except Exception as e:
            print(e)
            db.rollback()
            return jsonify(message ='Comment failed to post')


@bp.route('/<id>/likes', methods=['PUT', 'DELETE'])
@login_required
def like(id):
    db = get_db()
    method = request.method
    if method == 'PUT':
        try:
            newLike = Like(
                post_id = id,
                user_id = session.get('user_id')
            )
            db.add(newLike)
            db.commit()
        
        except Exception as e:
            print(e)
            db.rollback()
            return jsonify(message = 'Like failed'), 500

        return '', 204
    
    elif method == 'DELETE':
        try:
            like = db.query(Like).filter(Like.user_id == session.get('user_id'), Like.post_id == id).one()
            if like:
                db.delete(like)
                db.commit()
                return jsonify(message=True)
            else:
                return jsonify({'error': 'Please try again'})
        
        except Exception as e:
            print(e)
            db.rollback()
            return jsonify(message = 'Unlike failed'), 500