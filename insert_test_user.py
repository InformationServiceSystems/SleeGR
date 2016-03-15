from database import init
from databasemodels.models import User

db, dbe = init()
user = User('mail@test.de', '1234', 'Max', 'Mustermann')
user2 = User('liam@test.de', '1234')
db.insert_user(user)
db.insert_user(user2)