from datetime import datetime
from mapval import MappingValidator


correl_reference = {
    'A': ...,
    'Evening HR': lambda value: isinstance(value, type(None)) or isinstance(value, float),
    'Activity A': lambda value: isinstance(value, type(None)) or isinstance(value, float),
    'Load': lambda value: isinstance(value, type(None)) or isinstance(value, float),
    'time_stamp': datetime,
    'C': lambda value: isinstance(value, type(None)) or isinstance(value, float),
    'RPE': lambda value: isinstance(value, type(None)) or isinstance(value, int) or isinstance(value, float),
    'Deep sleep': lambda value: isinstance(value, type(None)) or isinstance(value, float),
    'Sleep length': lambda value: isinstance(value, type(None)) or isinstance(value, float),
    'T': lambda value: isinstance(value, type(None)) or isinstance(value, float),
    'Morning HR': lambda value: isinstance(value, type(None)) or isinstance(value, int) or isinstance(value, float),
    'Sleep start': lambda value: isinstance(value, type(None)) or isinstance(value, int),
    'Sleep end': lambda value: isinstance(value, type(None)) or isinstance(value, int),
    'DALDA': lambda value: isinstance(value, type(None)) or isinstance(value, float),
    'Activity G': lambda value: isinstance(value, type(None)) or isinstance(value, float),
    'Day of week': lambda value: isinstance(value, type(None)) or isinstance(value, int)
}




def correl_wrapper_gen(json):
    validator = MappingValidator(correl_reference)
    if validator.validate(json):
        return CorrelWrapper(json)
    else:
        return None


class CorrelWrapper:
    def __dir__(self):
        return ['a',
                'c',
                'dalda',
                'day_of_week',
                'deep_sleep',
                'evening_hr',
                'load',
                'morning_hr',
                'rpe',
                'sleep_end',
                'sleep_length',
                'sleep_start',
                't',
                'time_stamp']

    def __init__(self, json):
        self._correlation_json = json

    def a(self):
        return self._correlation_json['A']

    def dalda(self):
        return self._correlation_json['DALDA']

    def sleep_end(self):
        return self._correlation_json['Sleep end']

    def time_stamp(self):
        return self._correlation_json['time_stamp']

    def day_of_week(self):
        return self._correlation_json['Day of week']

    def sleep_length(self):
        return self._correlation_json['Sleep length']

    def activit_a(self):
        return self._correlation_json['Activity A']

    def activity_a(self):
        return self._correlation_json['Activity A']

    def activity_g(self):
        return self._correlation_json['Activity G']

    def t(self):
        return self._correlation_json['T']

    def evening_hr(self):
        return self._correlation_json['Evening HR']

    def rpe(self):
        return self._correlation_json['RPE']

    def sleep_start(self):
        return self._correlation_json['Sleep start']

    def morning_hr(self):
        return self._correlation_json['Morning HR']

    def c(self):
        return self._correlation_json['C']

    def deep_sleep(self):
        return self._correlation_json['Deep sleep']

    def load(self):
        return self._correlation_json['Load']


if __name__ == '__main__':
    date = datetime(2016, 1, 18, 11, 22, 55)

    json = {
        "A": 208.0867079039359,
        "Evening HR": None,
        "Activity A": 0.7630895933590968,
        "Load": 14300.577839859636,
        "time_stamp": date,
        "C": 68.72412939735467,
        "RPE": 5,
        "Deep sleep": 0.42857143,
        "Sleep length": 7.61,
        "T": -79.44353847749991,
        "Morning HR": 47,
        "Sleep start": -1,
        "Sleep end": 7,
        "DALDA": 1.5833333333333333,
        "Activity G": 0.049056262570958464,
        "Day of week": 2
    }
    res = correl_wrapper_gen(json)
    print(res)
