import database
from datetime import datetime
from mapval import MappingValidator

reference = {
    'Id': str,
    'type': int,
    'Measurement_Id': int,
    'time': str,
    'date': str,
    'tag': str,
    'val0': float,
    'val1': float,
    'val2': float
}


class Json2Mongo:
    def __init__(self):
        self._validator = MappingValidator(reference)
        self._db_inserts, self._db_extended = database.init()

    def _to_db(self, user, json):
        """
        JUST USE THIS METHOD IF YOU USED check_format!
        Better use check_and_commit
        """
        return self._db_inserts.insert_csv_row(user, json)

    def check_and_commit(self, json):
        if self._validator.validate(json):
            time_stamp_str = '%s,%s' % (json['date'],json['time'])
            new_json = {
                "tag": json['tag'],
                "UserID": json['Id'],
                "type": json['type'],
                "time_stamp": datetime.strptime(time_stamp_str, '%Y.%m.%d,%H:%M:%S'),
                "val1": json['val1'],
                "val2": json['val2'],
                "val0": json['val0']
            }
            return self._to_db(json['Id'], new_json)
        return False
