from flask import request, session
from webpage import app
from database import DataBaseEntry
from database import User

data_base_entry = DataBaseEntry()


@app.route('/')
def index():
    print('Hi')
    return 'Hello app'


@app.route('/login_rest', methods=['POST'])
def login():
    if request.method == 'POST':
        json_email_password = request.get_json()
        if data_base_entry.password_matches_email(json_email_password['email'],
                                                  json_email_password[
                                                      'password']):
            a = 2
            session['email'] = json_email_password['email']

        else:
            return 'fuck'
            #do other craze stuff


@app.route('/sign_rest', methods=['POST'])
def sign():
    if request.method == 'POST':
        json = request.get_json()
        user = User.decode(json)
        if user is not None:
            data_base_entry.insert_user(user)
        print('after creation')
        print(user)
    return "hi"
