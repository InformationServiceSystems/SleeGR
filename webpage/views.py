from datetime import datetime

import os
from flask import Flask, request, redirect, url_for, json, jsonify, session, render_template


import database
from databasemodels.models import User
from exceptions import InputError
from webpage import app
import names
from csvreader import csvReader
from decorators import login_required

db_inserts, db_extended = database.init()


@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))

@app.route('/loginn', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.values['email']
        password = request.values['password']
        if db_extended.password_matches_email(email, password):
            session['email'] = email
            return render_template('iot-triathlon-activity.html')
    return app.send_static_file('iot-login.html')

@app.route('/sign_rest', methods=['POST'])
def sign():
    if request.method == 'POST':
        json_new_user = request.get_json()
        json_new_user[names.type] = names.user_type_names.user_generals
        if not db_inserts.find_user(json_new_user[names.email]) == None:
            return jsonify(success=False, error_in='user', error_msg='user already exists')
        try:
            new_user = User.decode(json_new_user)
        except InputError as err:
            return jsonify(success=False, error_in=err.expression, error_msg=err.message)
        db_inserts.insert_user(new_user)
        return jsonify(success=True)
    return jsonify(success=False, error_in='request', error_msg='No post request sent')


@app.route('/show-stats/<user_id>/<start_date>/<end_date>/<measurement_type>')
def show_measurement(user_id, start_date, end_date, measurement_type):
    r = csvReader()
    start = datetime.strptime(start_date, '%Y-%d-%m')
    end = datetime.strptime(end_date, '%Y-%d-%m')
    if int(measurement_type) == 21:
        return json.dumps(r.heart_rate_sepecial(start, end))
    else:
        return json.dumps(r.read_data(user_id, start, end, measurement_type))

@app.route('/sleep_data/<user_id>/>start_date>/<end_date>')
def sleep_data(user_id, start_date, end_date):
    r = csvReader()
    start = datetime.strptime(start_date, '%Y-%d-%m')
    end = datetime.strptime(end_date, '%Y-%d-%m')
    return json.dumps(r.ReadSleepData(user_id, start,end))



UPLOAD_FOLDER = '/home/Flask/test1/uploads'
ALLOWED_EXTENSIONS = set(['bin','dat','csv','txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
"""
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
app.config['CORS_HEADERS'] = 'Content-Type'
"""



@app.route('/gaussian/<user_id>/<start_date>/<end_date>', methods=['GET'])
def gaussian(user_id, start_date, end_date):
    lst = []
    lst.append({'user_id':1, 'avg':0.5 , 'std':1.4})
    return json.dumps(lst)

@app.route('/gaussianPoints<user_id>/<start_date>/<end_date>')
def gaussianPoints(user_id, start_date, end_date):
    lst = []
    lst.append({'user_id':1, 'x':0.7 , 'y':3, 'date': '02.03.2016'})
    lst.append({'user_id':1, 'x':0.9 , 'y':2, 'date': '03.03.2016'})
    lst.append({'user_id':1, 'x':0.1 , 'y':1, 'date': '04.03.2016'})
    lst.append({'user_id':1, 'x':0.2 , 'y':4, 'date': '05.03.2016'})
    return json.dumps(lst)




@app.route('/sleepPoints')
def sleepPoints():
    lst = []
    lst.append({'user_id':1, 'x':7 , 'y':45})
    lst.append({'user_id':1, 'x':8.5 , 'y':35})
    lst.append({'user_id':1, 'x':8.3 , 'y':32})
    lst.append({'user_id':1, 'x':7.4 , 'y':39})
    lst.append({'user_id':1, 'x':3 , 'y':23})
    lst.append({'user_id':1, 'x':9 , 'y':43})
    lst.append({'user_id':1, 'x':10.2 , 'y':29})
    lst.append({'user_id':1, 'x':11 , 'y':17})
    lst.append({'user_id':1, 'x':6.4 , 'y':26})
    lst.append({'user_id':1, 'x':7.1 , 'y':43})
    lst.append({'user_id':1, 'x':9.4 , 'y':44})
    lst.append({'user_id':1, 'x':11.2 , 'y':26})
    lst.append({'user_id':1, 'x':5.5 , 'y':31})
    return json.dumps(lst)

@app.route('/son')
def typeACurve():
    lst = []
    lst.append({'user_id':1,'date':'03/14/2016', 'a':0.5 , 'b':1.4, 'c': 3, 'data_points':[{'x':4, 'y':10}, {'x':6, 'y':8}, {'x':11, 'y':13}]})
    lst.append({'user_id':1,'date':'03/15/2016', 'a':0.7 , 'b':1.2, 'c': 4, 'data_points':[{'x':6, 'y':12}, {'x':7, 'y':7}, {'x':13, 'y':17}]})
    lst.append({'user_id':1,'date':'03/16/2016', 'a':0.8 , 'b':1.1, 'c': 1, 'data_points':[{'x':3, 'y':3}, {'x':3, 'y':1}, {'x':12, 'y':18}, {'x':22, 'y':22},    {'x':30, 'y':5},{'x':33, 'y':8},{'x':56, 'y':10}]})
    lst.append({'user_id':1,'date':'03/17/2016', 'a':0.8 , 'b':1.1, 'c': 1, 'data_points':[{'x':3, 'y':3}, {'x':3, 'y':1}, {'x':12, 'y':18}]})
    lst.append({'user_id':1,'date':'03/11/2016', 'a':0.8 , 'b':1.1, 'c': 1, 'data_points':[{'x':3, 'y':3}, {'x':3, 'y':1}, {'x':12, 'y':18}]})
    lst.append({'user_id':1,'date':'03/12/2016', 'a':0.8 , 'b':1.1, 'c': 1, 'data_points':[{'x':3, 'y':3}, {'x':3, 'y':1}, {'x':12, 'y':18}]})
    lst.append({'user_id':1,'date':'03/10/2016', 'a':0.8 , 'b':1.1, 'c': 1, 'data_points':[{'x':3, 'y':3}, {'x':3, 'y':1}, {'x':12, 'y':18}]})
    lst.append({'user_id':1,'date':'03/09/2016', 'a':0.8 , 'b':1.1, 'c': 1, 'data_points':[{'x':3, 'y':3}, {'x':3, 'y':1}, {'x':12, 'y':18}]})
    lst.append({'user_id':1,'date':'03/08/2016', 'a':0.8 , 'b':1.1, 'c': 1, 'data_points':[{'x':3, 'y':3}, {'x':3, 'y':1}, {'x':12, 'y':18}]})
    lst.append({'user_id':1,'date':'03/07/2016', 'a':0.8 , 'b':1.1, 'c': 1, 'data_points':[{'x':3, 'y':3}, {'x':3, 'y':1}, {'x':12, 'y':18}]})
    lst.append({'user_id':1,'date':'03/06/2016', 'a':0.8 , 'b':1.1, 'c': 1, 'data_points':[{'x':3, 'y':3}, {'x':3, 'y':1}, {'x':12, 'y':18}]})
    lst.append({'user_id':1,'date':'03/05/2016', 'a':0.8 , 'b':1.1, 'c': 1, 'data_points':[{'x':3, 'y':3}, {'x':3, 'y':1}, {'x':12, 'y':18}]})
    return json.dumps(lst)

@app.route('/son2')
def typeBCurve():
    lst = []
    lst.append({'user_id':1,'date':'03/14/2016', 'a':0.2 , 'b':1.5, 'c': 3, 'data_points':[{'x':3, 'y':1}, {'x':9, 'y':8}, {'x':19, 'y':2}]})
    lst.append({'user_id':1,'date':'03/15/2016', 'a':0.1 , 'b':1.3, 'c': 2, 'data_points':[{'x':1, 'y':4}, {'x':8, 'y':7}, {'x':17, 'y':3}]})
    lst.append({'user_id':1,'date':'03/16/2016', 'a':0.4 , 'b':1.2, 'c': 2, 'data_points':[{'x':2, 'y':3}, {'x':1, 'y':1}, {'x':13, 'y':45}]})
    return json.dumps(lst)
    #return 'ok'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload2/<user_id>', methods=['GET', 'POST'])
def upload_file_seperately(user_id):
    path2save = '/home/Flask/test1/uploads/' + str(user_id)
    if not os.path.exists(path2save):
        os.makedirs(path2save)
        os.chmod(path2save, "0777")

    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            pass
            #filename = secure_filename(file.filename)
            #file.save(os.path.join(path2save, filename))
            #return redirect(url_for('uploaded_file',
            #                        filename=filename))
    return 'OK'


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            pass
            #filename = '''secure_filename('''file.filename()''')'''
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('uploaded_file',
            #                        filename=filename))
    return 'OK'


@app.route('/realtime',  methods=["GET"])
def getRealtimeHRM():
    hrm = request.args.get('hrm')
    return hrm


@app.route('/sendPost',  methods=["POST"])
def sendPost():
    return jsonify(request.get_json(force = True))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5555, threaded=True)

