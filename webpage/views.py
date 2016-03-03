from flask import request, session, redirect, url_for, jsonify

import database
from databasemodels.models import User
from exceptions import InputError
from webpage import app
import names

db_inserts, db_extended = database.init()


@app.route('/')
def index():
    #return app.send_static_file('index.html')
    return redirect(url_for('static', filename='index.html'))

@app.route('/login_rest', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        json_email_password = request.get_json()
        if db_extended.password_matches_email(json_email_password['email'],
                                                  json_email_password[
                                                      'password']):
            #session['email'] = json_email_password['email']
            return jsonify(success=True)
    return jsonify(success=False)

@app.route('/sign_rest', methods=['POST'])
def sign():
    if request.method == 'POST':
        json_new_user = request.get_json()
        if not db_inserts.find_user(json_new_user[names.email]) == None:
            return jsonify(success=False, error_in='user', error_msg='user already exists')
        try:
            new_user = User.decode(json_new_user)
        except InputError as err:
            return jsonify(success=False, error_in=err.expression, error_msg=err.message)
        db_inserts.insert_user(new_user)
        return jsonify(success=True)
    return jsonify(success=False, error_in='request', error_msg='No post request sent')

