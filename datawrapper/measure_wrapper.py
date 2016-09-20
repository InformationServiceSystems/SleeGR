from datawrapper.value_wrapper import ValueWrapper
from datetime import datetime

class MeasureWrapper:

    def __init__(self, measurement_json):
        self._measuremet_json = measurement_json

    @property
    def id(self):
        return self._measuremet_json['Id']

    @property
    def type(self):
        return self._measuremet_json['Type']

    @property
    def time_stamp(self):
        return self._measuremet_json['Time_stamp']

    def __getitem__(self, key):
        if isinstance(key, int) and key >= 0:
            return ValueWrapper(self._measuremet_json['values'][key])
        else:
            raise KeyError


date = datetime(2016,1,18,11,22,55)
json =  {
    'values': [{
        "type": 4,
        "email": "test@test.com",
        "tag": "Idle",
        "time_stamp": date,
        "val2": 0,
        "val1": 0,
        "val0": 1111
    },
    {
        "type": 4,
        "email": "test@test.com",
        "tag": "Idle",
        "time_stamp": date,
        "val2": 0,
        "val1": 0,
        "val0": 1112
    },
    {
        "type": 4,
        "email": "test@test.com",
        "tag": "Idle",
        "time_stamp": date,
        "val2": 0,
        "val1": 0,
        "val0": 1113
    }]
}

mw = MeasureWrapper(json)
for v in mw:
    print(v)