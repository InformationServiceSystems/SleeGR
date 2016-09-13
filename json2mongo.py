import database
from datetime import datetime
from mapval import MappingValidator

reference = {
    'ID': str,
    'type': int,
    'Measurement_ID': int,
    'time': str,
    'date': str,
    'tag': str,
    'val0': float,
    'val1': float,
    'val2': float
}


class Json2Mongo:
    def _to_db(self,json):
        """
        JUST USE THIS METHOD IF YOU USED check_format!
        Better use check_and_commit
        """
        self._validator = MappingValidator(reference)
        self._db_inserts.insert_csv_row(self._user, json)

    def check_and_commit(self, json):
        if self._validator.validate(json):
            time_stamp_str = '%s,%s' % (json['date'],json['time'])
            new_json = {
                "tag": json['tag'],
                "UserID": json['ID'],
                "type": json['val2'],
                "time_stamp": datetime.strptime(time_stamp_str, '%Y.%m.%d,%H:%M:%S'),
                "val1": json['val0'],
                "val2": json['val1'],
                "val0": 0
            }
            self._to_db(new_json)
