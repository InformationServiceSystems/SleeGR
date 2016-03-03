from database import init
from database import init, DbExtended, DbInserts
from databasemodels.models import User

class testDataBase():
    def __init__(self):
        self.entry , self.extended = init('test_database')
        self.user = User('testl@mail.de', '1234')
        self.entry.insert_user(self.user)
        self.user1 = User('test2@mail.de', '1234', 'Max', 'Mustermann')
        self.entry.insert_user(self.user1)
