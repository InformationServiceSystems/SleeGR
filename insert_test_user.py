from database import init
from databasemodels.models import User

db, dbe = init()
user = User('test@test.com', '123456')
db.insert_user(user)
