from flask import Blueprint, request, jsonify, session
from app.models import User
from app.db import get_db
import sys
from app.utils.helpers import get_user_posts

bp = Blueprint('users', __name__, url_prefix='/api/users')

@bp.route('/', methods=['GET'])
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
            user = db.query(User).filter(User.email == email).first()
            if user:
                if user.verify_password(password):
                    session['user_id'] = user.id
                    session['loggedIn'] = True
                    return jsonify({'message': 'Logged In!'}), 201
                else:
                    return jsonify({'error': 'Password is incorrect, please try again'})
            else:
                return jsonify({'error': 'There is no account with that email. Please signup to continue'}), 401
        else:
            return jsonify({'error': 'Please provide an email and password'}), 401
    except Exception as e:
        print (e)
        return jsonify({'error': 'Invalid form'})

@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return 'logged out', 204

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
        session['user_id'] = newUser.id
        session['loggedIn'] = True
        return jsonify({'message': 'Registered!'}), 201
    else:
        return make_response('User already exists. Please login', 202)
