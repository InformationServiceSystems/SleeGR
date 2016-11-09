from datetime import datetime
from statistics import mean, variance
import math
import S3_extract_dataset

from flask import request, redirect, json, session, make_response
import requests
from flask_cors import cross_origin


import database
from webpage import app
from authentification import requires_auth_api
from datareader import DataReader
from json2mongo import Json2Mongo

from dotenv import Dotenv
import os



env = None
try:
    env = Dotenv(os.path.dirname(os.path.realpath(__file__)) + '/.env')
except IOError:
    env = os.environ


db_inserts, db_extended = database.init()
j2m = Json2Mongo()


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


@app.route('/heartrate', methods=['POST'])
@requires_auth_api
def show_measurement():
    if request.method == 'POST':
        request_json = request.get_json()
        user_id = request_json['userId']
        type = request_json['type']
        start_date = request_json['beginDate']
        end_date = request_json['endDate']
        r = DataReader()
        start = datetime.strptime(start_date, '%d.%m.%Y')
        end = datetime.strptime(end_date, '%d.%m.%Y')
        response = make_response(json.dumps(r.heart_rate_special(user_id, start, end)))
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

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


@app.route('/sleepPoints', methods=['POST'])
@requires_auth_api
def sleep_data():
    if request.method == 'POST':
        request_json = request.get_json()
        user_id = request_json['userId']
        start_date = request_json['beginDate']
        end_date = request_json['endDate']
        gaussian_settings = request_json['gaussianSettings']
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
                response = make_response(json.dumps([{'user_id': user_id, 'avg': mean_duration, 'std': math.sqrt(variance_duration)}]))
                response.headers['Content-Type'] = 'application/json; charset=utf-8'
                return response
            else:
                response =  make_response(json.dumps([{'user_id': user_id, 'avg': -1000, 'std': 1}]))
                response.headers['Content-Type'] = 'application/json; charset=utf-8'
                return response
        else:
            response = make_response(json.dumps(r.read_sleep_data(user_id, start, end)))
            response.headers['Content-Type'] = 'application/json; charset=utf-8'
            return response


@app.route('/correlation', methods=['POST'])
@cross_origin()
@requires_auth_api
def correlations():
    if request.method == 'POST':
        request_json = request.get_json()
        user_id = request_json['userId']
        x_label = request_json['xAxis']
        y_label = request_json['yAxis']
        next_day =request_json['nextDay']
        cr = DataReader()
        response = make_response(json.dumps(cr.read_correlation_data(user_id, x_label, y_label, bool(next_day))))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/post_json', methods=['POST'])
@requires_auth_api
def receive_json():
    if request.method == 'POST':
        received_json = request.get_json()
        try:
            json_lst = []
            for list_entry in received_json['arrayOfMeasurements']:
                for le in list_entry['values']:
                    json_lst.append(le)
            if not j2m.check_and_commit_many(json_lst):
                return json.dumps({'status': 'failure'})
        except KeyError:
            return json.dumps({'status': 'failure'})
    S3_extract_dataset.run(received_json['arrayOfMeasurements'][0]['values'][0]['Id'])
    return json.dumps({'status': 'success'})


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', threaded=True)
