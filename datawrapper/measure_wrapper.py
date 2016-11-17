from datetime import datetime

from typing import Optional, Dict, List

from datawrapper import FHIR_objects
from datawrapper.value_wrapper import ValueWrapper, value_wrapper
from datawrapper.fhir_wrappers import observation_wrapper, ObservationWrapper


def value_list_validator(lst: List) -> bool:
    value_validator = FHIR_objects.MappingValidator(FHIR_objects.components_data)
    result = True
    for value in lst:
        result = result and value_validator.validate(value)
    return result

reference= {
    'Id': int,
    'Type': str,
    'Timestamp': str,
    'values': value_list_validator
}





class MeasureWrapper:
    def __init__(self, observation_wrapper: ObservationWrapper):
        self._observation_wrapper = observation_wrapper
        #self._measuremet_json = measurement_json

    @property
    def id(self) -> int:
        return self._observation_wrapper.identifier.value

    @property
    def type(self) -> str:
        return self._observation_wrapper.code.coding.display

    @property
    def time_stamp(self) -> datetime:
        return self._observation_wrapper.effectiveDateTime

    def __getitem__(self, key) -> ValueWrapper:
        if isinstance(key, int) and key >= 0:
            return value_wrapper(self._observation_wrapper.component[key])
        else:
            raise KeyError

value_validator = FHIR_objects.MappingValidator(reference)


def measure_wrapper(json: Dict) -> Optional[MeasureWrapper]:
    validator = FHIR_objects.MappingValidator(FHIR_objects.observation, FHIR_objects.ComparisonStyle.minimum)
    if validator.validate(json):
        return MeasureWrapper(observation_wrapper(json))
    else:
        return None

if __name__ == '__main__':
    date = datetime(2016, 1, 18, 11, 22, 55)
    date2 = datetime(2016, 1, 19, 11, 22, 55)
    measurements = {
        'arrayOfMeasurements': [
            {
                'Id': 1,
                'Type': 'bal',
                'Timestamp': '2016, 1, 18, 11, 22, 55',
                'values': [
                    {
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
                        "val1": date,
                        "val0": 1113
                    }]
            },
            {
                'Id': 2,
                'Type': 'bal',
                'Timestamp': '2016, 1, 19, 11, 22, 55',
                'values': [
                    {
                        "type": 4,
                        "email": "test@test.com",
                        "tag": "Idle",
                        "time_stamp": date2,
                        "val2": 0,
                        "val1": 0,
                        "val0": 1114
                    },
                    {
                        "type": 4,
                        "email": "test@test.com",
                        "tag": "Idle",
                        "time_stamp": date2,
                        "val2": 0,
                        "val1": 0,
                        "val0": 1115
                    },
                    {
                        "type": 4,
                        "email": "test@test.com",
                        "tag": "Idle",
                        "time_stamp": date2,
                        "val2": 0,
                        "val1": 0,
                        "val0": 1116
                    }]
            }
        ]

    }

    measures = measurements['arrayOfMeasurements']
    for measure in measures:
        res = measure_wrapper(measure)
        for elem in res:
            print(elem.time_stamp)

