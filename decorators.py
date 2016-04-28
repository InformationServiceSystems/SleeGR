from exceptions import InputError, error_messages
from validate_email import validate_email
from functools import wraps
from flask import session, redirect, url_for, request


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('email') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def check_user(f):
    def d(self, email, password, first_name=None, last_name=None):
        if not email or not validate_email(email):
            raise InputError(email, [2])
        if not password:
            raise InputError('Password', error_messages[3])
        if first_name:
            if not all(x.isalpha() or x.isspace() for x in first_name):
                raise InputError(first_name, error_messages[4])
        if last_name:
            if not last_name.isalpha():
                raise InputError(last_name, error_messages[4])
        f(self, email, password, first_name, last_name)
    return d


