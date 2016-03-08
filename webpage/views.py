import datetime
from flask import request, session, redirect, url_for, jsonify

import database
from databasemodels.models import User
from exceptions import InputError
from webpage import app
import names
from csvreader import csvReader

db_inserts, db_extended = database.init()


@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))

@app.route('/login_rest', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        json_email_password = request.get_json()
        if db_extended.password_matches_email(json_email_password['email'],
                                                  json_email_password[
                                                      'password']):
            session['email'] = json_email_password['email']
            return jsonify(success=True)
    return jsonify(success=False)

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
def show_measurement(user_id, start_date, end_date, workout_type):
    r = csvReader()
    return r.read_data(user_id, datetime.datetime(start_date), datetime.datetime(end_date), workout_type)


@app.route('/show-stats', methods=['GET'])
def show_measurement():
    if request.method == 'GET':
        r = csvReader()
        return r.read_data(request.data['user_id'], datetime(request.data['start_date']), datetime(request.data['end_date']), request.data['workout_type'])