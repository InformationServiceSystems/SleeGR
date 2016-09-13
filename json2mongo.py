import database
import datetime

from mapval import MappingValidator
reference_json = {
    'ID': str,
    'type': int,
    'date': str,

}
class JsonValidator:

    def __init__(self, user, pattern):
        self._user = user
        self._pattern = pattern

    def check_and_commit(self, json):
        if self.check_format(json):
            if self.check_types(json):
                self._to_db(json)

    def check_format(self, json):
        result = True
        for key in json:
            result = result and (key in self._pattern)
        for key in self._pattern:
            result = result and (key in json)
        return result

    def check_types(self,json):
        """
        ID: string
        type: int
        time_stamp: string
        date: string
        tag: string
        val0: floats
        val1: floats
        val2: floats
        """
        result = True
        for j in json:
            result = result and type(json[j]) == self._pattern[j]
        return result


class Json2Mongo:

    def __init__(self):
        self._validator = MappingValidator()

    def _to_db(self,json):
        """
        JUST USE THIS METHOD IF YOU USED check_format!
        Better use check_and_commit
        """
        self._db_inserts.insert_csv_row(self._user, json)

    def check_and_commit(self, json):
        if self.check_format(json):
            if self.check_types(json):
                self._to_db(json)



if __name__ == '__main__':
    json =  {'UserID': 'Matthias', 'type': 1,
                            'time_stamp': datetime.datetime.today(), 'tag': 'Cooldown',
                            'val0': 0.0 , 'val1': 1.0, 'val2': 1.0}
    pattern =  {'UserID': str, 'type': int,
                            'time_stamp': datetime.datetime, 'tag': str,
                            'val0':float , 'val1':float, 'val2': float}
    j2m = Json2Mongo(json, 'Matthias', pattern)
    print(j2m.check_format())