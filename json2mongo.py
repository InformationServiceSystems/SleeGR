import database
from datetime import datetime
from mapval import MappingValidator
import re

reference = {
    'Id': str,
    'type': int,
    'Measurement_Id': int,
    'time': str,
    'date': str,
    'tag': str,
    'val0': lambda val: type(val) is int or type(val) is float,
    'val1': lambda val: type(val) is int or type(val) is float,
    'val2': lambda val: type(val) is int or type(val) is float
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
        new_json = self.check(json)
        if new_json:
            return self._to_db(new_json['UserID'], new_json)

    def check(self, json):
        if self._validator.validate(json):
            time_stamp_str = '%s,%s' % (json['date'],json['time'])
            new_json = {
                "tag": json['tag'],
                "UserID": json['Id'].replace('_at_', '@'),
                "type": json['type'],
                "time_stamp": datetime.strptime(time_stamp_str, '%Y.%m.%d,%H:%M:%S'),
                "val1": json['val1'],
                "val2": json['val2'],
                "val0": json['val0']
            }
            return new_json
        return None

    def check_many(self, json_lst):
        bulk = []
        for json in json_lst:
            new_json = self.check(json)
            if new_json:
                bulk.append(new_json)
            else:
                return None
        if not bulk:
            return None
        return bulk

    def _to_db_many(self, user, json_lst):
        return self._db_inserts.insert_csv_row_many(user, json_lst)

    def check_and_commit_many(self, json_lst):
        new_json_lst = self.check_many(json_lst)
        if new_json_lst:
            return self._to_db_many(new_json_lst[0]['UserID'], new_json_lst)