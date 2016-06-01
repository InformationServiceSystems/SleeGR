import datetime

from database import init
from databasemodels.models import User
from csv_2_mongo import csv_2_reader
import sys

sys.path.append('.')
db, dbe = init()
user = User('test@test.com', '123456')
db.insert_user(user)
csv = csv_2_reader()
csv.transfer_data('test@test.com', datetime(2016, 1, 1), datetime(2016, 3, 31), 21)
