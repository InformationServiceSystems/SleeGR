from database.databaseentry import DataBaseEntry
from databasemodels.models import User
db = DataBaseEntry()
user = User('mail@test.de', '1234', 'Max', 'Mustermann')
user2 = User('liam@test.de')
db.insert_user(user)
db.insert_user(user2)