from datetime import datetime
from typing import Optional, List, Union
from mapval import MappingValidator, ComparisonStyle
from datawrapper import FHIR_objects

def _generator(sample, reference, cls):
    validator = MappingValidator(reference, ComparisonStyle.maximum)
    if validator.validate(sample):
        return cls(sample)
    else:
        return None

def iso_date2str(date_string: Union[str, datetime]) -> Optional[datetime]:
    if isinstance(date_string, datetime):
        return date_string
    try:
        return datetime.strptime(date_string, '%Y.%m.%dT%H:%M:%S')
    except ValueError:
        pass
    try:
        parts = date_string.split(' ')
        return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S ' + parts[1])
    except ValueError:
        pass


class PeriodWrapper:
    def __init__(self, json):
        self._period_json = json

    @property
    def end(self) -> datetime:
        return self._period_json['end']

    @property
    def start(self) -> datetime:
        return self._period_json['start']


def period_wrapper(json) -> Optional[PeriodWrapper]:
    return _generator(json, FHIR_objects.period, PeriodWrapper)


class ReferenceWrapper:
    def __init__(self, json):
        self._fhir_reference_reference_json = json

    @property
    def display(self) -> str:
        return self._fhir_reference_reference_json['display']

    @property
    def reference(self) -> Optional[str]:
        return self._fhir_reference_reference_json['reference']


def reference_wrapper(json) -> Optional[ReferenceWrapper]:
    return _generator(json, FHIR_objects.fhir_reference_reference, ReferenceWrapper)


class CodingWrapper():
    def __init__(self, json):
        self._coding_json = json

    @property
    def version(self) -> Optional[str]:
        return self._coding_json['version']

    @property
    def code(self) -> Optional[str]:
        return self._coding_json['code']

    @property
    def system(self) -> Optional[str]:
        return self._coding_json['system']

    @property
    def userSelected(self) -> Optional[bool]:
        return self._coding_json['userSelected']

    @property
    def display(self) -> Optional[str]:
        return self._coding_json['display']


def coding_wrapper(json) -> Optional[CodingWrapper]:
    return _generator(json, FHIR_objects.coding, CodingWrapper)


class CodeableConceptWrapper:
    def __init__(self, json):
        self._codeable_concept_json = json

    @property
    def coding(self) -> Optional[List[CodingWrapper]]:
        coding_list = self._codeable_concept_json['coding']
        result_list = []
        for coding in coding_list:
            result_list.append(coding_wrapper(coding))
        return result_list

    @property
    def text(self) -> Optional[str]:
        return self._codeable_concept_json['text']


def codeable_concept_wrapper(json) -> Optional[CodeableConceptWrapper]:
    return _generator(json, FHIR_objects.codeable_concept, CodeableConceptWrapper)


class QuantityWrapper:
    def __init__(self, json):
        self._quantity_json = json
    @property
    def value(self) -> float:
        return self._quantity_json['value']

    @property
    def comparator(self) -> Optional[str]:
        return self._quantity_json['comparator']

    @property
    def unit(self) -> [Optional[str]]:
        return self._quantity_json['unit']

    @property
    def system(self) -> Optional[str]:
        return self._quantity_json['system']

    @property
    def code(self) -> Optional[str]:
        return self._quantity_json['code']


def quantity_wrapper(json):
    return _generator(json, FHIR_objects.quantity, QuantityWrapper)


class RatioWrapper:
    def __init__(self, json):
        self._ratio_json = json

    @property
    def numerator(self) -> QuantityWrapper:
        return QuantityWrapper(self._ratio_json['numerator'])

    @property
    def denominator(self) -> QuantityWrapper:
        return QuantityWrapper(self._ratio_json['denominator'])


def ratio_wrapper(json)-> Optional[RatioWrapper]:
    return _generator(json, FHIR_objects.ratio, RatioWrapper)


class IdentifierWrapper:
    def __init__(self, json):
        self._identifier_json = json

    @property
    def value(self):
        return self._identifier_json['value']

    @property
    def period(self) -> Optional[PeriodWrapper]:
        return period_wrapper(self._identifier_json['period'])

    @property
    def use(self) -> str:
        return self._identifier_json['use']

    @property
    def assigner(self) -> Optional[str]:
        return self._identifier_json['assigner']

    @property
    def type(self) -> Optional[CodeableConceptWrapper]:
        return codeable_concept_wrapper(self._identifier_json['type'])

    @property
    def system(self) -> Optional[str]:
        return self._identifier_json['system']


def identifier_wrapper(json) -> Optional[IdentifierWrapper]:
    return _generator(json, FHIR_objects.identifier, IdentifierWrapper)


class ComponentsDataWrapper:
    def __init__(self, json):
        self._components_data_json = json

    @property
    def code(self) -> CodeableConceptWrapper:
        return codeable_concept_wrapper(self._components_data_json['code'])

    @property
    def valueString(self) -> Optional[str]:
        return self._components_data_json['valueString']

    @property
    def referenceRange(self) -> None:
        return self._components_data_json['referenceRange']

    @property
    def valueTime(self) -> None:
        return self._components_data_json['valueTime']

    @property
    def valueCodeableConcept(self) -> Optional[CodeableConceptWrapper]:
        return self._components_data_json['valueCodeableConcept']

    @property
    def valueRatio(self) -> None:
        return self._components_data_json['valueRatio']

    @property
    def valueDateTime(self) -> datetime:
        value = self._components_data_json['valueDateTime']
        if isinstance(value, str):
            return iso_date2str(value)
        elif isinstance(value, datetime):
            return value
        else:
            return None

    @property
    def dataAbsentReason(self) -> None:
        return self._components_data_json['dataAbsentReason']

    @property
    def valueAttachment(self) -> None:
        return self._components_data_json['valueAttachment']

    @property
    def valueRange(self) -> None:
        return self._components_data_json['valueRange']

    @property
    def valueQuantity(self) -> QuantityWrapper:
        return quantity_wrapper(self._components_data_json['valueQuantity'])

    @property
    def valueSampledData(self) -> None:
        return self._components_data_json['valueSampledData']

    @property
    def valuePeriod(self) -> None:
        return self._components_data_json['valuePeriod']


def components_data_wrapper(json) -> Optional[ComponentsDataWrapper]:
    return _generator(json, FHIR_objects.components_data, ComponentsDataWrapper)


class ObservationWrapper:
    def __init__(self, json):
        self._observation_json = json

    @property
    def interpretation(self) -> None:
        return self._observation_json['interpretation']

    @property
    def subject(self) -> ReferenceWrapper:
        return reference_wrapper(self._observation_json['subject'])

    @property
    def code(self) -> Optional[CodeableConceptWrapper]:
        return codeable_concept_wrapper(self._observation_json['code'])

    @property
    def component(self) -> List[ComponentsDataWrapper]:
        result_list = []
        components_list = self._observation_json['component']
        for component in components_list:
            result_list.append(components_data_wrapper(component))
        return result_list


    @property
    def related(self) -> None:
        return self._observation_json['related']

    @property
    def referenceRange(self) -> None:
        return self._observation_json['referenceRange']

    @property
    def valueTime(self) -> None:
        return self._observation_json['valueTime']

    @property
    def valueCodeableConcept(self) -> None:
        return self._observation_json['valueCodeableConcept']

    @property
    def valueQuantity(self) -> None:
        return self._observation_json['valueQuantity']

    @property
    def specimen(self) -> None:
        return self._observation_json['specimen']

    @property
    def dataAbsentReason(self) -> None:
        return self._observation_json['dataAbsentReason']

    @property
    def effectiveDateTime(self) -> datetime:
        value = self._observation_json['effectiveDateTime']
        if isinstance(value, str):
            return iso_date2str(value)
        elif isinstance(value, datetime):
            return  value
        else:
            return None

    @property
    def category(self) -> Optional[CodeableConceptWrapper]:
        return codeable_concept_wrapper(self._observation_json['category'])

    @property
    def valueRange(self) -> None:
        return self._observation_json['valueRange']

    @property
    def resourceType(self) -> str:
        return self._observation_json['resourceType']

    @property
    def valueDateTime(self) -> None:
        return self._observation_json['valueDateTime']

    @property
    def valuePeriod(self) -> None:
        return self._observation_json['valuePeriod']

    @property
    def status(self) -> str:
        return self._observation_json['status']

    @property
    def valueString(self) -> None:
        return self._observation_json['valueString']

    @property
    def issued(self) -> None:
        return self._observation_json['issued']

    @property
    def identifier(self) -> IdentifierWrapper:
        return identifier_wrapper(self._observation_json['identifier'])

    @property
    def effectivePeriod(self) -> PeriodWrapper:
        return period_wrapper(self._observation_json['effectivePeriod'])

    @property
    def valueRatio(self) -> None:
        return self._observation_json['valueRatio']

    @property
    def performer(self) -> None:
        return self._observation_json['performer']

    @property
    def comments(self) -> str:
        return self._observation_json['comments']

    @property
    def valueAttachment(self) -> None:
        return self._observation_json['valueAttachment']

    @property
    def device(self) -> ReferenceWrapper:
        return self._observation_json['device']

    @property
    def method(self) -> None:
        return self._observation_json['method']

    @property
    def valueSampledData(self) -> None:
        return self._observation_json['valueSampledData']

    @property
    def encounter(self) -> None:
        return self._observation_json['encounter']

    @property
    def bodySite(self) -> None:
        return self._observation_json['bodySite']


def observation_wrapper(json) -> Optional[ObservationWrapper]:
    return _generator(json, FHIR_objects.observation, ObservationWrapper)

