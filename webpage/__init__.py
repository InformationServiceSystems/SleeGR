from flask import Flask
from flask.ext.cors import CORS
import sys

sys.path.append('../')
app = Flask(__name__)
CORS(app)
app.config.from_object('settings')
import webpage.views

app.debug = True
app.run(host='0.0.0.0', port=80)
#app.run()
