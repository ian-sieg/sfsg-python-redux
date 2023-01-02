from flask import session, redirect
from functools import wraps

def login_required(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        if session.get('loggedIn') == True:
            return func(*args, **kwargs)
        # might have to change this given we're not serving up templates anymore
        return redirect('/home')
    return wrapped_function