from datetime import datetime
from statistics import mean, variance
import re
import math
import S3_extract_dataset

import os
from flask import Flask, request, redirect, url_for, json, jsonify, session, render_template, send_from_directory
import requests
from flask_cors import CORS, cross_origin

from linear_datascience import Comp1D

import database
from databasemodels.models import User
from exceptions import InputError
from webpage import app
import names
from decorators import login_required
from authentification import requires_BASEAuth, requires_auth_api
from datareader import DataReader
from json2mongo import Json2Mongo, reference
import bcrypt

from datawrapper import measure_wrapper, value_wrapper
from dotenv import Dotenv
import os



env = None
try:
    env = Dotenv(os.path.dirname(os.path.realpath(__file__)) + '/.env')
except IOError:
    env = os.environ


db_inserts, db_extended = database.init()
j2m = Json2Mongo()


@app.route("/")
@app.route("/login")
def home():
    return render_template('iot-login-auth0.html', env=env)

# Here we're using the /callback route.
@app.route('/callback')
def callback_handling():

  code = request.args.get('code')

  json_header = {'content-type': 'application/json'}

  token_url = "https://{domain}/oauth/token".format(domain=env['AUTH0_DOMAIN'])

  token_payload = {
      'client_id': env['AUTH0_CLIENT_ID'], \
      'client_secret': env['AUTH0_CLIENT_SECRET'], \
      'redirect_uri': env['AUTH0_CALLBACK_URL'], \
      'code': code, \
      'grant_type': 'authorization_code' \
      }

  token_info = requests.post(token_url, data=json.dumps(token_payload), headers = json_header).json()

  try:
      user_url = "https://{domain}/userinfo?access_token={access_token}" \
        .format(domain=env["AUTH0_DOMAIN"], access_token=token_info['access_token'])
  except KeyError:
      return redirect('/')


  user_info = requests.get(user_url).json()

  # We're saving all user information into the session
  session['profile'] = user_info

  # Redirect to the User logged in page that you want here
  # In our case it's /dashboard
  return redirect('/dashboard')

@app.route('/oldLogin', methods=['POST', 'GET'])
def login():
    error = None
    if request.args.get('next'):
        session['next'] = request.args.get('next', None)
    if request.method == 'POST':
        email = request.values['email']
        password = request.values['password']
        if db_extended.password_matches_email(email, password):
            profile = {'email': email}
            session['profile'] = profile
            if 'next' in session:
                next = session.get('next')
                session.pop('next')
                return redirect(next)
            return redirect(url_for("dashboard"))
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


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        email = request.values['email']
        password = bcrypt.hashpw(request.values['password'].encode(), bcrypt.gensalt())
        fullname = request.values['name']
        import re
        name_list = re.split(' ', fullname)
        firstname = ''
        lastname = ''
        if len(name_list) == 0:
            lastname = None
            firstname = None
        elif len(name_list) == 1:
            firstname = None
            if not name_list[0]:
                lastname = name_list[0]
            else:
                lastname = None
        else:
            lastname = name_list[-1]
            del (name_list[-1])
            firstname = ' '.join(name_list)
        new_user = User(email, password, first_name=firstname, last_name=lastname)
        db_inserts.insert_user(new_user)
        return redirect(url_for("login"))
    return app.send_static_file('iot-register.html')


@app.route('/heartrate', methods=['POST'])
@requires_auth_api
def show_measurement():
    if request.method == 'POST':
        user_id = request.values['userId']
        type = request.values['type']
        start_date = request.values['beginDate']
        end_date = request.values['endDate']
        r = DataReader()
        start = datetime.strptime(start_date, '%d.%m.%Y')
        end = datetime.strptime(end_date, '%d.%m.%Y')
        return json.dumps(r.heart_rate_special(user_id, start, end))

@app.route('/get_correlations_list', methods=['GET'])
@cross_origin()
@requires_auth_api
def get_correlations_list():
    to_reply = '[{"x_label": "Day of week", "y_label": "Sleep length", "next_day": false}, ' \
            '{"x_label": "Sleep length", "y_label": "Load", "next_day": false},' \
            '{"x_label": "Sleep start", "y_label": "Load", "next_day": false},' \
            '{"x_label": "Sleep end", "y_label": "Load", "next_day": false},' \
            '{"x_label": "Sleep length", "y_label": "Deep sleep", "next_day": false},' \
            '{"x_label": "Deep sleep", "y_label": "Load", "next_day": false},' \
            '{"x_label": "Load", "y_label": "Deep sleep", "next_day": true},' \
            '{"x_label": "Load", "y_label": "Activity A", "next_day": false},' \
            '{"x_label": "Load", "y_label": "Activity G", "next_day": false},' \
            '{"x_label": "RPE", "y_label": "Deep sleep", "next_day": true},' \
            '{"x_label": "RPE", "y_label": "Load", "next_day": false},' \
            '{"x_label": "DALDA", "y_label": "Deep sleep", "next_day": true},' \
            '{"x_label": "Sleep end", "y_label": "RPE", "next_day": false},' \
            '{"x_label": "Sleep length", "y_label": "RPE", "next_day": false}]'
    return to_reply

@app.route('/dashboard')
@login_required
def dashboard():
    user = session['profile']
    return render_template('iot-triathlon-activity.html', user=user, url=env['GLOBAL_URL'])

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

@app.route('/sleepPoints', methods=['POST'])
@requires_auth_api
def sleep_data():
    if request.method == 'POST':
        user_id = request.values['userId']
        start_date = request.values['beginDate']
        end_date = request.values['endDate']
        gaussian_settings = str2bool(request.values['gaussianSettings'])
        r = DataReader()
        start = datetime.strptime(start_date, '%d.%m.%Y')
        end = datetime.strptime(end_date, '%d.%m.%Y')
        if gaussian_settings:
            sleep_data = r.read_sleep_data(user_id, start, end)
            average_list = []
            var_list = []
            for data in sleep_data:
                average_list.append(data['x'])
                var_list.append(data['y'])
            if len(average_list) > 1 and len(var_list) > 1:
                mean_duration = mean(average_list)
                variance_duration = variance(average_list)
                return json.dumps([{'user_id': user_id, 'avg': mean_duration, 'std': math.sqrt(variance_duration)}])
            else:
                return json.dumps([{'user_id': user_id, 'avg': -1000, 'std': 1}])
        else:
            return json.dumps(r.read_sleep_data(user_id, start, end))




@app.route('/profile')
@login_required
def profile():
    return render_template('iot-triathlon-profile.html', user=session['profile'])

@app.route('/correlation', methods=['POST'])
@cross_origin()
@requires_auth_api
def correlations():
    if request.method == 'POST':
        user_id = request.values['userId']
        x_label = request.values['xAxis']
        y_label = request.values['yAxis']
        next_day = request.values['nextDay']
        cr = DataReader()
        return json.dumps(cr.read_correlation_data(user_id, x_label, y_label, bool(next_day)))


UPLOAD_FOLDER = '/home/Flask/test1/uploads'
ALLOWED_EXTENSIONS = set(['bin', 'dat', 'csv', 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


@app.route('/post_json', methods=['POST'])
@requires_auth_api
def receive_json():
    if request.method == 'POST':
        received_json = request.get_json()
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(received_json)
        for received_json in received_json['arrayOfFhirObservations']:
            #received_json = received_json['arrayOfFhirObservations'][0]
            print(type(received_json['effectiveDateTime']), received_json['effectiveDateTime'])
            try:
                received_wrapper = measure_wrapper.measure_wrapper(received_json)
                print(received_wrapper)
                if not received_wrapper:
                    raise KeyError
                db_inserts.insert_measure(received_wrapper)
            except KeyError:
                return json.dumps({'status': 'failure'})
    S3_extract_dataset.run(received_wrapper.observation_wrapper.subject.display) #TODO username
    return json.dumps({'status': 'failure'})
    #return json.dumps({'status': 'success'})



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/signout')
@login_required
def signout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', threaded=True)
