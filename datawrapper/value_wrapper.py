class ValueWrapper:

    def __init__(self, json):
        self._json = json

    @property
    def val0(self):
        return self._json['val0']

    @property
    def val1(self):
        return self._json['val1']

json =
vw = ValueWrapper()