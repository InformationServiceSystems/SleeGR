from datetime import datetime
from typing import Optional, Union, Dict
from datawrapper import FHIR_objects
from mapval import ComparisonStyle
from datawrapper.fhir_wrappers import components_data_wrapper, ComponentsDataWrapper, ObservationWrapper


# value_reference = {
#         "type": int,
#         "email": str,
#         "tag": str,
#         "time_stamp": datetime,
#         "val2": lambda val: isinstance(val, float) or isinstance(val, int),
#         "val1": lambda val: isinstance(val, float) or isinstance(val, int) or isinstance(val, datetime),
#         "val0": lambda val: isinstance(val, float) or isinstance(val, int)
#     }

class ValueWrapper:
    def __init__(self, component_wrapper: ComponentsDataWrapper, observation_wrapper: ObservationWrapper):
        self._observation = observation_wrapper
        self._component_wrapper = component_wrapper
        #self._value_json = json

    def __repr__(self):
        return str(self._component_wrapper)

    @property
    def val0(self) -> Optional[Union[int, float]]:
        return self._component_wrapper.valueQuantity.value
        # return self._value_json['val0']

    @property
    def val1(self) -> Optional[Union[int, float, datetime]]:
        return self._component_wrapper.valueQuantity.value
        # return self._value_json['val1']

    @property
    def val2(self) -> Optional[Union[int, float]]:
        return self._component_wrapper.valueQuantity.value
        # return self._value_json['val2']

    @property
    def email(self) -> str:
        return  self._observation.subject.display

    @property
    def time_stamp(self) -> datetime:
        return self._component_wrapper.valueDateTime
        # return  self._value_json['time_stamp']

    @property
    def tag(self) -> str:
        return self._observation.category.coding[0].display

    @property
    def type(self) -> str:
        return self._component_wrapper.code.coding[0].display


def value_wrapper(json: Dict) -> Optional[ValueWrapper]:
    validator = FHIR_objects.MappingValidator(FHIR_objects.components_data, comparison_style=ComparisonStyle.maximum)
    if validator.validate(json):
        return ValueWrapper(components_data_wrapper(json))
    else:
        return None

def value_wrapper(json: Dict, observation_warpper: ObservationWrapper) -> Optional[ValueWrapper]:
    validator = FHIR_objects.MappingValidator(FHIR_objects.components_data, comparison_style=ComparisonStyle.maximum)
    if validator.validate(json):
        return ValueWrapper(components_data_wrapper(json), observation_warpper)
    else:
        return None


if __name__ == '__main__':
    pass
