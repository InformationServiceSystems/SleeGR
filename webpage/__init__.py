from flask import Flask
from flask_cors import CORS
import sys
from dotenv import Dotenv
import os

env = None
try:
    env = Dotenv(os.path.dirname(os.path.realpath(__file__)) + '/.env')
except IOError:
    env = os.environ

sys.path.append('../')
app = Flask(__name__)
CORS(app)
app.config.from_object('settings')
import webpage.views

app.debug = True
app.run(host='0.0.0.0', port=int(env['PORT']))
#app.run()
