from flask import request, session, redirect, send_from_directory, render_template, url_for
from webpage import app
from database import DataBaseEntry
from database import User

data_base_entry = DataBaseEntry()


@app.route('/')
def index():
    #return app.send_static_file('index.html')
    return redirect(url_for('static', filename='index.html'))

@app.route('/login_rest', methods=['POST'])
def login():
    if request.method == 'POST':
        json_email_password = request.get_json()
        print(json_email_password)
        if data_base_entry.password_matches_email(json_email_password['email'],
                                                  json_email_password[
                                                      'password']):
            print('success')
            '''session['email'] = json_email_password['email']'''
            return redirect(url_for('static', filename='index.html'))
    return redirect(url_for('static', filename='dashboard/index.html'))


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
