from flask import Flask

app = Flask(__name__, static_url_path='')
app.config.from_object('settings')
import webpage.views


app.run(host='0.0.0.0')