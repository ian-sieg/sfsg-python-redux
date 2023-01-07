from flask import Blueprint, request, jsonify, make_response, session
from app.models import User, Post
from app.db import get_db
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import uuid
import sys
from app.utils.helpers import get_user, get_user_posts

# from app.models.User import token_required
from dotenv import load_dotenv
from os import getenv

load_dotenv()
secret = getenv('SECRET_KEY')

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/users', methods = ['GET'])
def get_users():
    db = get_db()
    users = db.query(User).all()
    output = []
    
    for user in users:
        output.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'posts': get_user_posts(user.id)
        })
    
    return jsonify({'users': output})

@bp.route('/login', methods = ['POST'])
def login():
    db = get_db()
    data = request.get_json()
    email = data['email']
    password = data['password']
    try:
        if (email and password):
            user = db.query(User).filter(User.email == data['email']).first()
            if user:
                if user.verify_password(password):
                    token = create_access_token(identity=user.id)
                    return jsonify({'token': token}), 201
                else:
                    return jsonify({'error': 'Password is incorrect, please try again'})
            else:
                return jsonify({'error': 'There is no account with that email. Please signup to continue'}), 401
        else:
            return jsonify({'error': 'Please provide an email and password'}), 401
    except Exception as e:
        print (e)
        return jsonify({'error': 'Invalid form'})

@bp.route('/register', methods = ['POST'])
def signup():
    data = request.get_json()
    db = get_db()
    
    username = data['username']
    email = data['email']
    password = data['password']
    
    user = db.query(User)\
        .filter_by(email = email)\
        .first()
    
    if not user:
        try:
            newUser = User(
                id=str(uuid.uuid4()),
                username=username,
                email=email,
                password=password
            )
            token = create_access_token(identity=newUser.id)
            db.add(newUser)
            db.commit()
        
        except:
            print(sys.exc_info())
            db.rollback()
            return jsonify(message = 'Signup failed'), 500
        
        session.clear()
        session['user_id'] = newUser.id
        
        return jsonify({'token': token}), 201
    else:
        return make_response('User already exists. Please login', 202)

@bp.route('/posts', methods = ['GET'])
def get_posts():
    db = get_db()
    posts = db.query(Post).all()
    return [{
            "id": i.id,
            "title": i.title,
            "content": i.content,
            "user_id": i.user_id,
            'user': get_user(i.user_id),
            'created_at': i.created_at,
            'updated_at': i.updated_at
    } for i in posts]

@bp.route('/post/new', methods=['POST'])
@jwt_required()
def new_post():
    data = request.get_json()
    db = get_db()

    title = data['title']
    content = data['content']
    user_id = data['user_id']
    
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

@bp.route('/post/<id>', methods=['PUT', 'DELETE'])
@jwt_required()
def posts(id):
    method = request.method
    db = get_db()
    
    if (method == 'DELETE'):
        try:
            post = db.query(Post).filter(Post.id == id).one()
            db.delete(post)
            db.commit()
            return jsonify({'success': True})
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
                user_id = data['user_id']
                # TODO: add authentication so only the user with their id stored in the session can == post.user_id
                post.title = title
                post.content = content
                db.commit()
                return jsonify({'success': 'true'})
            else:
                return jsonify({'error': 'No post with this id'})
        except Exception as e:
            print(e)
            return jsonify({'error': 'Invalid form'})