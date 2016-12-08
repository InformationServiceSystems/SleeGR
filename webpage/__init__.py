from flask import Flask
from flask_cors import CORS
import sys
from dotenv import load_dotenv
import os

env = None
try:
    env = load_dotenv(os.path.dirname(os.path.realpath(__file__)) + '/.env')
except IOError:
    env = os.environ

sys.path.append('../')
app = Flask(__name__)
CORS(app)
app.config.from_object('settings')
import webpage.views

app.debug = True
app.run(host='0.0.0.0', port=int(os.environ.get('PORT')), threaded=True)
#app.run()
