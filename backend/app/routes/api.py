from flask import Blueprint, request, jsonify, make_response, session
from app.models import User
from app.db import get_db
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
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
    email = data['email']
    password = data['password']
    try:
        if (email and password):
            user = db.query(User).filter(User.email == data['email']).first()
            if user:
                if user.verify_password(password):
                    token = create_access_token(identity=user.public_id)
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
    
    # if not data or not data['email'] or not data['password']:
    #     return jsonify(message = 'Please provide your email and password'), 401
    
    # try:
    #     user = db.query(User).filter(User.email == data['email']).one()
    # except:
    #     print(sys.exc_info())
    #     return jsonify(message = 'There is no account with that email. Please signup to continue'), 401

    # if user.verify_password(data['password']) == False:
    #     return jsonify(message = 'Incorrect password'), 403
    # else:
    #     token = create_access_token(identity=user["id"])
    #     return jsonify({"token": token})
    # session.clear()
    # session['user_id'] = user.public_id
    # session['loggedIn'] = True
    
    # return jsonify(message = 'You have been logged in!'), 201

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
