from datetime import datetime, timedelta

from typing import Optional, Dict, List

from datawrapper import FHIR_objects
from datawrapper.value_wrapper import ValueWrapper, value_wrapper
from datawrapper.fhir_wrappers import *
from datawrapper.test_fhir_obj import observation_example

import S3_extract_dataset


def value_list_validator(lst: List) -> bool:
    value_validator = FHIR_objects.MappingValidator(FHIR_objects.components_data)
    result = True
    for value in lst:
        result = result and value_validator.validate(value)
    return result


reference = {
    'Id': int,
    'Type': str,
    'Timestamp': str,
    'values': value_list_validator
}


class MeasureWrapper:
    def __init__(self, observation_wrapper: ObservationWrapper):
        self._observation_wrapper = observation_wrapper
        self._components = self._observation_wrapper.component
        # self._measuremet_json = measurement_json

    def __repr__(self):
        return str(self.observation_wrapper._observation_json)

    @property
    def observation_wrapper(self):
        return self._observation_wrapper

    @property
    def id(self) -> int:
        return self._observation_wrapper.identifier.value

    @property
    def type(self) -> str:
        return self._observation_wrapper.category.coding.pop().display

    @property
    def time_stamp(self) -> datetime:
        return self._observation_wrapper.effectiveDateTime

    def __getitem__(self, key) -> ValueWrapper:
        if isinstance(key, int) and key >= 0:
            return value_wrapper(self._components[key]._components_data_json, self.observation_wrapper)
        else:
            raise KeyError


value_validator = FHIR_objects.MappingValidator(reference)


def measure_wrapper(json: Dict) -> Optional[MeasureWrapper]:
    validator = FHIR_objects.MappingValidator(FHIR_objects.observation, FHIR_objects.ComparisonStyle.maximum)
    if validator.validate(json):
        json['effectiveDateTime'] = iso_date2str(json['effectiveDateTime'])
        return MeasureWrapper(observation_wrapper(json))
    else:
        return None


if __name__ == '__main__':
    date = datetime(2016, 1, 18, 11, 22, 55)
    date2 = datetime(2016, 1, 19, 11, 22, 55)

    measures = observation_example['arrayOfObservations']
    for measure in measures:
        res = measure_wrapper(measure)

        import database

        db_inserts, db_extended = database.init()
        dct = {}
        db_inserts.insert_measure(res)
        date = datetime(2016, 11, 14)
        res_bal = db_extended.find_data_tag(res.observation_wrapper.subject.display, 'Accelerometer', 'TrainingHR')
        S3_extract_dataset.run(res.observation_wrapper.subject.display)
        print(res_bal)





