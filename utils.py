import jwt
from dotenv import load_dotenv
import os
import base64


env = os.environ

client_id = env['AUTH0_CLIENT_ID']
client_secret = env['AUTH0_CLIENT_SECRET']

def handle_deafult(fhir_object, token):
    payload = jwt.decode(
        token,
        base64.b64decode(client_secret.replace("_", "/").replace("-", "+")),
        audience=client_id
    )
    print(payload)
    return