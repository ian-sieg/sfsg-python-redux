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
        return make_response(
            # login issue is here first
            'Could not verify 1',
            401,
            {'WWW-Authenticate': 'Basic realm = "Login required"'}
        )
    user = db.query(User)\
        .filter_by(email = data['email'])\
        .first()
    
    if not user:
        return make_response(
            'Could not verify 2',
            401,
            {'WWW-Authenticate': 'Basic realm = "User does not exist"'}
        )
    
    # if check_password_hash(user.password, data['password']):
    #     token = jwt.encode(
    #         payload = {
    #             'public_id': user.public_id,
    #             'exp': datetime.now() + timedelta(minutes=120)
    #         }, 
    #         key = secret,
    #     )
    #     print('HIIIIIIIIIIIII')
    #     print(jwt.decode(token, key=secret, algorithms=['HS256', ]))
    #     print('BYYEEEEEEEEEE')
    #     # decoded = jwt.decode(token, key=secret, )
    #     return make_response(jsonify({'token': token.decode('UTF-8')}), 201)
    
    return make_response(
        'Could not verify 3',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password"'}
    )

@bp.route('/signup', methods = ['POST'])
def signup():
    data = request.get_json()
    db = get_db()
    
    public_id = str(uuid.uuid4())
    username = data['username']
    email = data['email']
    password = data['password']
    
    user = db.query(User)\
        .filter_by(email = email)\
        .first()
    
    if not user:
        try:
            newUser = User(
                public_id=public_id,
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
