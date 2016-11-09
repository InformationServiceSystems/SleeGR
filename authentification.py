import database
from functools import wraps
from flask import request, Response, session, redirect, jsonify,_request_ctx_stack
from werkzeug.local import LocalProxy
import base64
import jwt
import os
from dotenv import Dotenv

db_inserts, db_extended = database.init()
env = None

try:
    env = Dotenv(os.path.dirname(os.path.realpath(__file__)) + '/webpage/.env')
    client_id = env["AUTH0_CLIENT_ID"]
    client_secret = env["AUTH0_CLIENT_SECRET"]
except IOError:
  env = os.environ

def check_auth(username, password):
    return db_extended.password_matches_email(username, password)

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_BASEAuth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# Authentication annotation
current_user = LocalProxy(lambda: _request_ctx_stack.top.current_user)

# Authentication attribute/annotation
def authenticate_error(error):
  resp = jsonify(error)
  resp.status_code = 401
  return resp

def requires_auth_api(f):
  @wraps(f)
  def decorated(*args, **kwargs):

    auth = request.headers.get('Authorization', None)
    if not auth:
      return authenticate_error({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'})
    parts = auth.split()
    if parts[0].lower() != 'bearer':
      return authenticate_error({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'})
    elif len(parts) == 1:
      return authenticate_error({'code': 'invalid_header', 'description': 'Token not found'})
    elif len(parts) > 2:
      return authenticate_error({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'})
    token = parts[1]
    try:
        payload = jwt.decode(
            token,
            base64.b64decode(client_secret.replace("_","/").replace("-","+")),
            audience=client_id
        )
    except jwt.ExpiredSignature:
        return authenticate_error({'code': 'token_expired', 'description': 'token is expired'})
    except jwt.InvalidAudienceError:
        return authenticate_error({'code': 'invalid_audience', 'description': 'incorrect audience, expected: ' + client_id})
    except jwt.DecodeError:
        return authenticate_error({'code': 'token_invalid_signature', 'description': 'token signature is invalid'})
    _request_ctx_stack.top.current_user = user = payload
    return f(*args, **kwargs)
  return decorated
