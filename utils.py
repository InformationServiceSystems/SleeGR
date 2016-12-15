import jwt
from dotenv import load_dotenv
import os
import base64
import requests
from flask import json



env = os.environ

client_id = env['AUTH0_CLIENT_ID']
client_secret = env['AUTH0_CLIENT_SECRET']

try:
    proxy = env['PROXY']
except KeyError:
    proxy=None

proxyDict = {
    'http': proxy,
    'https': proxy,
    'ftp': proxy
}

def get_user_info(auth):
    parts = auth.split()
    token = parts[1]
    payload = jwt.decode(
        token,
        base64.b64decode(client_secret.replace("_", "/").replace("-", "+")),
        audience=client_id
    )
    token_url = "https://{domain}/api/v2/users/{user_id}".format(domain=env['AUTH0_DOMAIN'], user_id=payload['sub'])
    data = {
        'include_fields':'false'
    }

    json_header = {
        'authorization' : 'Bearer ' + env['AUTH0_KEY'],
        'content-type': 'application/json'
    }
    user = requests.get(token_url, params=json.dumps(data), headers=json_header, proxies=proxyDict).json()

    return user