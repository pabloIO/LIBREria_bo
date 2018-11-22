from functools import wraps
from flask import g, request, redirect, url_for, render_template

def cookie_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # print(request.headers['Content-Type'])
        # print('middlware')
        token = request.cookies.get('token') 
        if not token:
            return render_template('index.html'), 400
        return f(*args, **kwargs)
    return decorated_function