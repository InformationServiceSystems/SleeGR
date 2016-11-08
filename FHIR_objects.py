from datetime import datetime

def string_comparator(string_comp:str, *str_lst) -> bool:
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

identifier = {
    # from Element: extension
    'use': lambda code: string_comparator(code, ['usual', 'official', 'temp']) ,  # usual | official | temp | secondary (If known)
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
        #'valueCodeableConcept': codeable_concept,
        'valueDateTime': datetime,
        # Provides guide for interpretation of component result
    }

def components_list_validator (components_list: List[Dict])-> bool:
    value_validator = MappingValidator(components_data)
    result = True
    for value in components_list:
        result = result and value_validator.validate(value)
    return result

observation = {
    'resourceType': lambda string: string == 'Observation',
    # from Resource: id, meta, implicitRules, and language
    # from DomainResource: text, contained, extension, and modifierExtension
    'identifier': identifier,  # Unique Id for this particular observation
    'status': 'code',  # R!  registered | preliminary | final | amended +
    'code': codeable_concept,  # R!  Type of observation (code / type)
    'subject': '-- Reference(Patient) --',  # Who and/or what this is about
    # effective[x]: Clinically relevant time/time-period for observation. One of these 2:
    'effectiveDateTime': datetime,
    'effectivePeriod': period,
    # Who is responsible for the observation
    # value[x]: Actual result. One of these 10:
    'device': '-- Reference(Device) --',  # (Measurement) Device
    'component': [components_data]
}

import pprint
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(observation)
