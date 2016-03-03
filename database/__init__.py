from database.dbextendend import DbExtended
from database.dbinserts import DbInserts
from database.database import DbBase


def init(db_name='triathlon'):
    database = DbBase(db_name)
    return DbInserts(database), DbExtended(database)