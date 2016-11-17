from datetime import datetime
from typing import Dict, List
from mapval import MappingValidator, ComparisonStyle

def word_in_list(string_comp:str, *str_lst) -> bool:
    for string in str_lst:
        if string == string_comp:
            return True
    return False

period = {
    # from Element: extension
    'start': datetime,  # C? Starting time with inclusive boundary
    'end': datetime  # C? End time with inclusive boundary, if not ongoing
}

coding = {
    # from Element: extension
    'system': str,  # Identity of the terminology system
    'version': str,  # Version of the system - if relevant
    'code': str,  # Symbol in syntax defined by the system
    'display': str,  # Representation defined by the system
    'userSelected': bool  # If this coding was chosen directly by the user
}

fhir_reference_reference = {
    # from Element: extension
    'reference': ...,  # C? Relative, internal or absolute URL reference
    'display': 'string'  # Text alternative for the resource
}

quantity = {
    # from Element: extension
    'value': float,  # Numerical value (with implicit precision)
    'comparator': '<code>',  # < | <= | >= | > - how to understand the value
    'unit': lambda unit : unit == 'bpm',  #TODO insert other possible values # Unit representation
    'system': '<uri>',  # C? System that defines coded unit form
    'code': '<code>'  # Coded form of the unit
}

ratio = {
    # from Element: extension
    'numerator': quantity,  # Numerator value
    'denominator': quantity  # Denominator value
}

codeable_concept = {
    # from Element: extension
    'coding': coding,  # Code defined by a terminology system
    'text': str  # Plain text representation of the concept
}

identifier_use = ['usual', 'official', 'temp']

identifier = {
    # from Element: extension
    'use': lambda code: word_in_list(code, identifier_use) ,  # usual | official | temp | secondary (If known)
    'type': codeable_concept,  # Description of identifier
    'system': str,  # The namespace for the identifier
    'value': str,  # The value that is unique
    'period': period,  # Time period when id is/was valid for use
    'assigner': '-- Reference(Organization) --'  # Organization that issued id (may be just text)
}

components_data = {  # Component results
        'code': codeable_concept,  # C? R!  Type of component observation (code / type)
        # value[x]: Actual component result. One of these 10:
        'valueQuantity': quantity,
        'valueCodeableConcept': ...,
        'valueString': ...,
        'valueRange': ...,
        'valueRatio': ...,
        'valueSampledData': ...,
        'valueAttachment': ...,
        'valueTime': ...,
        'valueDateTime': datetime,
        'valuePeriod': ...,
        'dataAbsentReason': ...,  # C? Why the component result is missing
        'referenceRange': ...
    }


def components_validator (components_list: List[Dict])-> bool:
    value_validator = MappingValidator(components_data)
    result = True
    for value in components_list:
        result = result and value_validator.validate(value)
    return result

observation_code = ['registered', 'preliminary', 'final', 'amended']
observation = {
    'resourceType': lambda string: string == 'Observation',
    # from Resource: id, meta, implicitRules, and language
    # from DomainResource: text, contained, extension, and modifierExtension
    'identifier': identifier,  # Unique Id for this particular observation
    'status': lambda code: word_in_list(code, observation_code),  # R!  registered | preliminary | final | amended +
    'category': ...,  # Classification of  type of observation
    'code': codeable_concept,  # R!  Type of observation (code / type)
    'subject': '-- Reference(Patient) --',  # Who and/or what this is about
    'encounter': ...,  # Healthcare event during which this observation is made
    # effective[x]: Clinically relevant time/time-period for observation. One of these 2:
    'effectiveDateTime': str,
    'effectivePeriod': period,
    'issued': ...,  # Date/Time this was made available
    'performer': ...,
    # Who is responsible for the observation
    # value[x]: Actual result. One of these 10:
    'valueQuantity':        ...,
    'valueCodeableConcept': ...,
    'valueString':          ...,
    'valueRange':           ...,
    'valueRatio':           ...,
    'valueSampledData':     ...,
    'valueAttachment':      ...,
    'valueTime':            ...,
    'valueDateTime':        ...,
    'valuePeriod':          ...,
    'dataAbsentReason':     ...,                        # C? Why the result is missing
    'interpretation':       ..., # High, low, normal, etc.
    'comments':             ..., # Comments about result
    'bodySite':             ..., # Observed body part
    'method':               ..., # How it was done
    'specimen':             ...,  # Specimen used for this observation
    'device':               fhir_reference_reference, # (Measurement) Device
    'component': components_validator,
    'referenceRange': ..., # Provides guide for interpretation
    'related': ..., # Resource related to this observation'
}
if __name__ == '__main__':
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(observation)
