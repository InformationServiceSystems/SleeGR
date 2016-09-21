from pymongo import MongoClient#
import bcrypt
client = MongoClient('localhost', 27017)
db = client['triathlon']


def update():
    for user in db.general_user.find():
        id = user['_id']
        password = user['password']
        db.general_user.update_one({'_id':id}, {'$set':{'password':bcrypt.hashpw(password.encode(), bcrypt.gensalt())}})

update()