class Correlwrapper:
    def __init__(self, json):
        self._correlation_json = json

    @property
    def a(self):
        return self._correlation_json['A']

    @property
    def dalda(self):
        return self._correlation_json['DALDA']

    @property
    def sleep_end(self):
        return self._correlation_json['Sleep end']

    @property
    def time_stamp(self):
        return self._correlation_json['time-stamp']

    @property
    def day_of_week(self):
        return self._correlation_json['Day of week']

    @property
    def sleep_length(self):
        return self._correlation_json['Sleep length']

    @property
    def activit_a(self):
        return self._correlation_json['Activity A']

    @property
    def activity_a(self):
        return self._correlation_json['Activity A']

    @property
    def activity_g(self):
        return self._correlation_json['Activity G']

    @property
    def t(self):
        return self._correlation_json['T']

    @property
    def evening_hr(self):
        return self._correlation_json['Evening HR']

    @property
    def rpe(self):
        return self._correlation_json['RPE']

    @property
    def sleep_start(self):
        return self._correlation_json['Sleep start']

    @property
    def morning_hr(self):
        return self._correlation_json['morning HR']

    @property
    def c(self):
        return self._correlation_json['C']

    @property
    def deep_sleep(self):
        return self._correlation_json['Deep sleep']

    @property
    def load(self):
        return self._correlation_json['Load']
