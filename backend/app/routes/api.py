from flask import Blueprint, request, jsonify, make_response, session
from app.models import User
from app.db import get_db
from datetime import datetime, timedelta
import uuid
import sys

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
            'public_id': user.public_id,
            'username': user.username,
            'email': user.email
        })
    
    return jsonify({'users': output})

@bp.route('/login', methods = ['POST'])
def login():
    db = get_db()
    data = request.get_json()
    
    if not data or not data['email'] or not data['password']:
        return jsonify(message = 'Please provide your email and password'), 401
    
    try:
        user = db.query(User).filter(User.email == data['email']).one()
    except:
        print(sys.exc_info())
        return jsonify(message = 'There is no account with that email. Please signup to continue'), 401

    if user.verify_password(data['password']) == False:
        return jsonify(message = 'Incorrect password'), 403
    
    session.clear()
    session['user_id'] = user.public_id
    session['loggedIn'] = True
    
    return jsonify(message = 'You have been logged in!'), 201

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
                public_id=str(uuid.uuid4()),
                username=username,
                email=email,
                password=password
            )
            print('HIIIIII')
            print(newUser)
            print('BYEEEEE')
            db.add(newUser)
            db.commit()
        
        except:
            print(sys.exc_info())
            db.rollback()
            return jsonify(message = 'Signup failed'), 500
        
        session.clear()
        session['user_id'] = newUser.public_id
        
        return make_response('Successfully registered.', 201)
    else:
        return make_response('User already exists. Please login', 202)
