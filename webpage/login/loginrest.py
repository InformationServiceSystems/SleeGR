from flask import request
from webpage import app
from database.models import User


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        pass


@app.route('/registration', methods=['POST'])
def registration():
    if request.method == 'POST':
        pass
        #create new user an insert to database

