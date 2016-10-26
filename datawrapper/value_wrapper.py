from datetime import datetime
from mapval import MappingValidator
value_reference = {
        "type": int,
        "email": str,
        "tag": str,
        "time_stamp": datetime,
        "val2": lambda val: isinstance(val, float) or isinstance(val, int),
        "val1": lambda val: isinstance(val, float) or isinstance(val, int),
        "val0": lambda val: isinstance(val, float) or isinstance(val, int)
    }


def value_wrapper_gen(json):
    validator = MappingValidator(value_reference)
    if validator.validate(json):
        return ValueWrapper(json)
    else:
        return None


class ValueWrapper:
    def __init__(self, json):
        self._value_json = json

    def __repr__(self):
        return str(self._value_json)

    @property
    def val0(self):
        return self._value_json['val0']

    @property
    def val1(self):
        return self._value_json['val1']

    @property
    def val2(self):
        return self._value_json['val2']

    @property
    def email(self):
        return self._value_json['email']

    @property
    def time_stamp(self):
        return  self._value_json['time_stamp']

    @property
    def tag(self):
        return self._value_json['tag']

    @property
    def type(self):
        return self._value_json['type']


if __name__ == '__main__':
    date = datetime(2016,1,18,11,22,55)

    json = {
        "type": 4,
        "email": "test@test.com",
        "tag": "Idle",
        "time_stamp": date,
        "val2": 0,
        "val1": 0,
        "val0": 1111
    }

    vw = value_wrapper_gen(json)

    print(vw.val0)
