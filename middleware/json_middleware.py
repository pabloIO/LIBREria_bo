from functools import wraps
from flask import g, request, redirect, url_for, render_template

def json_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # print(request.headers['Content-Type'])
        # print('middlware')
        if not request.is_json:
            return render_template('errors/400.html'), 400
        return f(*args, **kwargs)
    return decorated_function