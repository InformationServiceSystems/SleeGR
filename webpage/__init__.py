from flask import Flask

app = Flask(__name__)
app.config.from_object('settings')
import webpage.views


app.run(host='0.0.0.0')
#   app.run()