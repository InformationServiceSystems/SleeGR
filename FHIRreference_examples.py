fhir_observation_reference = {
    'resourceType': 'Observation',
    # from Resource: id, meta, implicitRules, and language
    # from DomainResource: text, contained, extension, and modifierExtension
    'identifier': ['-- Identifier --'],  # Unique Id for this particular observation
    'status': 'code',  # R!  registered | preliminary | final | amended +
    'category': '-- CodeableConcept --',  # Classification of  type of observation
    'code': '-- CodeableConcept --',  # R!  Type of observation (code / type)
    'subject': '-- Reference(Patient|Group|Device|Location) --',  # Who and/or what this is about
    'encounter': '-- Reference(Encounter) --',  # Healthcare event during which this observation is made
    # effective[x]: Clinically relevant time/time-period for observation. One of these 2:
    'effectiveDateTime': 'dateTime',
    'effectivePeriod': '-- Period --',
    'issued': 'instant',  # Date/Time this was made available
    'performer': ['-- Reference(Practitioner|Organization|Patient|RelatedPerson) --'],
    # Who is responsible for the observation
    # value[x]: Actual result. One of these 10:
    'valueQuantity': '-- Quantity --',
    'valueCodeableConcept': '-- CodeableConcept --',
    'valueString': 'string',
    'valueRange': '-- Range --',
    'valueRatio': '-- Ratio --',
    'valueSampledData': '-- SampledData --',
    'valueAttachment': '-- Attachment --',
    'valueTime': 'time',
    'valueDateTime': 'dateTime',
    'valuePeriod': '-- Period --',
    'dataAbsentReason': '-- CodeableConcept --',  # C? Why the result is missing
    'interpretation': '-- CodeableConcept --',  # High, low, normal, etc.
    'comments': 'string',  # Comments about result
    'bodySite': '-- CodeableConcept --',  # Observed body part
    'method': '-- CodeableConcept --',  # How it was done
    'specimen': '-- Reference(Specimen) --',  # Specimen used for this observation
    'device': '-- Reference(Device|DeviceMetric) --',  # (Measurement) Device
    'referenceRange': [{  # Provides guide for interpretation
        'low': '-- Quantity(SimpleQuantity) --',  # C? Low Range, if relevant
        'high': '-- Quantity(SimpleQuantity) --',  # C? High Range, if relevant
        'meaning': '-- CodeableConcept --',  # Indicates the meaning/use of this range of this range
        'age': '-- Range --',  # Applicable age range, if relevant
        'text': 'string'  # Text based reference range in an observation
    }],
    'related': [{  # Resource related to this observation'
        'type': 'code',  # has-member | derived-from | sequel-to | replaces | qualified-by | interfered-by
        'target': '-- Reference(Observation|QuestionnaireResponse) --'  # R!  Resource that is related to this one
    }],
    'component': [{  # Component results
        'code': '-- CodeableConcept --',  # C? R!  Type of component observation (code / type)
        # value[x]: Actual component result. One of these 10:
        'valueQuantity': '-- Quantity --',
        'valueCodeableConcept': '-- CodeableConcept --',
        'valueString': 'string',
        'valueRange': '-- Range --',
        'valueRatio': '-- Ratio --',
        'valueSampledData': '-- SampledData --',
        'valueAttachment': '-- Attachment --',
        'valueTime': 'time',
        'valueDateTime': 'dateTime',
        'valuePeriod': '-- Period --',
        'dataAbsentReason': '-- CodeableConcept --',  # C? Why the component result is missing
        'referenceRange': ['-- Content as for Observation.referenceRange --']
        # Provides guide for interpretation of component result
    }]
}

fhir_identifier_reference = {
    # from Element: extension
    'use': 'code',  # usual | official | temp | secondary (If known)
    'type': '--CodeableConcept --',  # Description of identifier
    'system': 'uri',  # The namespace for the identifier
    'value': 'string',  # The value that is unique
    'period': '-- Period --',  # Time period when id is/was valid for use
    'assigner': '-- Reference(Organization) --'  # Organization that issued id (may be just text)
}

fhir_codeable_concept_reference = {
    # from Element: extension
    'coding': ['-- Coding --'],  # Code defined by a terminology system
    'text': 'string'  # Plain text representation of the concept
}

fhit_coding_reference = {
    # from Element: extension
    'system': 'uri',  # Identity of the terminology system
    'version': 'string',  # Version of the system - if relevant
    'code': 'code',  # Symbol in syntax defined by the system
    'display': 'string',  # Representation defined by the system
    'userSelected': 'boolean'  # If this coding was chosen directly by the user
}

fhir_period_reference = {
    # from Element: extension
    'start': 'dateTime',  # C? Starting time with inclusive boundary
    'end': 'dateTime'  # C? End time with inclusive boundary, if not ongoing
}

fhir_reference_reference = {
    # from Element: extension
    'reference': 'string',  # C? Relative, internal or absolute URL reference
    'display': 'string'  # Text alternative for the resource
}

fhir_organization_reference = {
    'resourceType': 'Organization',
    # from Resource: id, meta, implicitRules, and language
    # from DomainResource: text, contained, extension, and modifierExtension
    'identifier': ['-- Identifier --'],  # C? Identifies this organization  across multiple systems
    'active': 'boolean',  # Whether the organization's record is still in active use
    'type': '-- CodeableConcept --',  # Kind of organization
    'name': 'string',  # C? Name used for the organization
    'telecom': ['-- ContactPoint --'],  # C? A contact detail for the organization
    'address': ['-- Address --'],  # C? An address for the organization
    'partOf': '-- Reference(Organization) --',  # The organization of which this organization forms a part
    'contact': [{  # Contact for the organization for a certain purpose
        'purpose': '-- CodeableConcept --',  # The type of contact
        'name': '-- HumanName --',  # A name associated with the contact
        'telecom': ['-- ContactPoint --'],  # Contact details (telephone, email, etc.)  for a contact
        'address': '-- Address --'  # Visiting or postal addresses for the contact
    }]
}

fhir_contact_point_reference = {
    'resourceType': 'ContactPoint',
    # from Element: extension
    'system': 'code',  # C? phone | fax | email | pager | other
    'value': 'string',  # The actual contact point details
    'use': 'code',  # home | work | temp | old | mobile - purpose of this contact point
    'rank': 'positiveInt',  # Specify preferred order of use (1 = highest)
    'period': '-- Period --'  # Time period when the contact point was/is in use
}

fhir_address_reference = {
    'resourceType': 'Address',
    # from Element: extension
    'use': 'code',  # home | work | temp | old - purpose of this address
    'type': 'code',  # postal | physical | both
    'text': 'string',  # Text representation of the address
    'line': ['string'],  # Street name, number, direction & P.O. Box etc.
    'city': 'string',  # Name of city, town etc.
    'district': 'string',  # District name (aka county)
    'state': 'string',  # Sub-unit of country (abbreviations ok)
    'postalCode': 'string',  # Postal code for area
    'country': 'string',  # Country (can be ISO 3166 3 letter code)
    'period': '-- Period --'  # Time period when address was/is in use
}

fhir_human_name_reference = {
    'resourceType': 'HumanName',
    # from Element: extension
    'use': 'code',  # usual | official | temp | nickname | anonymous | old | maiden
    'text': 'string',  # Text representation of the full name
    'family': ['string'],  # Family name (often called 'Surname')
    'given': ['string'],  # Given names (not always 'first'). Includes middle names
    'prefix': ['string'],  # Parts that come before the name
    'suffix': ['string'],  # Parts that come after the name
    'period': '-- Period --'  # Time period when name was/is in use
}

fhir_patient_reference = {
    'resourceType': 'Patient',
    # from Resource: id, meta, implicitRules, and language
    # from DomainResource: text, contained, extension, and modifierExtension
    'identifier': ['-- Identifier --'],  # An identifier for this patient
    'active': 'boolean',  # Whether this patient's record is in active use
    'name': ['-- HumanName --'],  # A name associated with the patient
    'telecom': ['-- ContactPoint --'],  # A contact detail for the individual
    'gender': 'code',  # male | female | other | unknown
    'birthDate': 'date',  # The date of birth for the individual
    # deceased[x]: Indicates if the individual is deceased or not. One of these 2:
    'deceasedBoolean': 'boolean',
    'deceasedDateTime': 'dateTime',
    'address': ['-- Address --'],  # Addresses for the individual
    'maritalStatus': '-- CodeableConcept --',  # Marital (civil) status of a patient
    # multipleBirth[x]: Whether patient is part of a multiple birth. One of these 2:
    'multipleBirthBoolean': 'boolean',
    'multipleBirthInteger': 'integer',
    'photo': ['-- Attachment --'],  # Image of the patient
    'contact': [{  # A contact party (e.g. guardian, partner, friend) for the patient
        'relationship': ['-- CodeableConcept --'],  # The kind of relationship
        'name': '-- HumanName --',  # A name associated with the contact person
        'telecom': ['-- ContactPoint --'],  # A contact detail for the person
        'address': '-- Address --',  # Address for the contact person
        'gender': 'code',  # male | female | other | unknown
        'organization': '-- Reference(Organization) --',  # C? Organization that is associated with the contact
        'period': '-- Period --'
        # The period during which this contact person or organization is valid to be contacted relating to this patient
    }],
    'animal': {  # This patient is known to be an animal (non-human)
        'species': '-- CodeableConcept --',  # R!  E.g. Dog, Cow
        'breed': '-- CodeableConcept --',  # E.g. Poodle, Angus
        'genderStatus': '-- CodeableConcept --'  # E.g. Neutered, Intact
    },
    'communication': [{  # A list of Languages which may be used to communicate with the patient about his or her health
        'language': '-- CodeableConcept --',
        # R!  The language which can be used to communicate with the patient about his or her health
        'preferred': 'boolean'  # Language preference indicator
    }],
    'careProvider': ['-- Reference(Organization|Practitioner) --'],  # Patient's nominated primary care provider
    'managingOrganization': '-- Reference(Organization) --',  # Organization that is the custodian of the patient record
    'link': [{  # Link to another patient resource that concerns the same actual person
        'other': '-- Reference(Patient) --',  # R!  The other patient resource that the link refers to
        'type': 'code'  # R!  replace | refer | seealso - type of link
    }]
}

fhir_group_reference = {
    'resourceType': 'Group',
    # from Resource: id, meta, implicitRules, and language
    # from DomainResource: text, contained, extension, and modifierExtension
    'identifier': ['-- Identifier --'],  # Unique id
    'type': '<code>',  # R!  person | animal | practitioner | device | medication | substance
    'actual': '<boolean>',  # C? R!  Descriptive or actual
    'code': '-- CodeableConcept --',  # Kind of Group members
    'name': '<string>',  # Label for Group
    'quantity': '<unsignedInt>',  # Number of members
    'characteristic': [{  # Trait of group members
        'code': '-- CodeableConcept --',  # R!  Kind of characteristic
        # value[x]: Value held by characteristic. One of these 4:
        'valueCodeableConcept': '-- CodeableConcept --',
        'valueBoolean': '<boolean>',
        'valueQuantity': '-- Quantity --',
        'valueRange': '-- Range --',
        'exclude': '<boolean>',  # R!  Group includes or excludes
        'period': '-- Period --'  # Period over which characteristic is tested
    }],
    'member': [{  # C? Who or what is in group
        'entity': '--{ Reference(Patient|Practitioner|Device|Medication|Substance) --',
        # R!  Reference to the group member
        'period': '-- Period --',  # Period member belonged to the group
        'inactive': '<boolean>'  # If member is no longer in group
    }]
}

fhir_range_reference = {
    # from Element: extension
    'low': '-- Quantity(SimpleQuantity) --',  # C? Low limit
    'high': '-- Quantity(SimpleQuantity) --'  # C? High limit
}

fhir_quantity_referecne = {
    # from Element: extension
    'value': '<decimal>',  # Numerical value (with implicit precision)
    'comparator': '<code>',  # < | <= | >= | > - how to understand the value
    'unit': '<string>',  # Unit representation
    'system': '<uri>',  # C? System that defines coded unit form
    'code': '<code>'  # Coded form of the unit
}

fhir_device_reference = {
    'resourceType': 'Device',
    # from Resource: id, meta, implicitRules, and language
    # from DomainResource: text, contained, extension, and modifierExtension
    'identifier': ['-- Identifier --'],  # Instance id from manufacturer, owner, and others
    'type': '-- CodeableConcept --',  # R!  What kind of device this is
    'note': ['-- Annotation --'],  # Device notes and comments
    'status': '<code>',  # available | not-available | entered-in-error
    'manufacturer': '<string>',  # Name of device manufacturer
    'model': '<string>',  # Model id assigned by the manufacturer
    'version': '<string>',  # Version number (i.e. software)
    'manufactureDate': '<dateTime>',  # Manufacture date
    'expiry': '<dateTime>',  # Date and time of expiry of this device (if applicable)
    'udi': '<string>',  # FDA mandated Unique Device Identifier
    'lotNumber': '<string>',  # Lot number of manufacture
    'owner': '-- Reference(Organization) --',  # Organization responsible for device
    'location': '-- Reference(Location) --',  # Where the resource is found
    'patient': '-- Reference(Patient) --',  # If the resource is affixed to a person
    'contact': ['-- ContactPoint --'],  # Details for human/organization for support
    'url': '<uri>'  # Network address to contact device
}

fhir_annotation_reference = {
    # from Element: extension
    # author[x]: Individual responsible for the annotation. One of these 2:
    'authorReference': '-- Reference(Practitioner|Patient|RelatedPerson) --',
    'authorString': '<string>',
    'time': '<dateTime>',  # When the annotation was made
    'text': '<string>'  # R!  The annotation  - text content
}

fhir_practitioner_reference = {
    'resourceType': 'Practitioner',
    # from Resource: id, meta, implicitRules, and language
    # from DomainResource: text, contained, extension, and modifierExtension
    'identifier': ['-- Identifier --'],  # A identifier for the person as this agent
    'active': '<boolean>',  # Whether this practitioner's record is in active use
    'name': '-- HumanName --',  # A name associated with the person
    'telecom': ['-- ContactPoint --'],  # A contact detail for the practitioner
    'address': ['-- Address --'],  # Where practitioner can be found/visited
    'gender': '<code>',  # male | female | other | unknown
    'birthDate': '<date>',  # The date  on which the practitioner was born
    'photo': ['-- Attachment --'],  # Image of the person
    'practitionerRole': [{  # Roles/organizations the practitioner is associated with
        'managingOrganization': '-- Reference(Organization) --',  # Organization where the roles are performed
        'role': '-- CodeableConcept --',  # Roles which this practitioner may perform
        'specialty': ['-- CodeableConcept --'],  # Specific specialty of the practitioner
        'period': '-- Period --',  # The period during which the practitioner is authorized to perform in these role(s)
        'location': ['-- Reference(Location) --'],  # The location(s) at which this practitioner provides care
        'healthcareService': ['-- Reference(HealthcareService) --']
        # The list of healthcare services that this worker provides for this role's Organization/Location(s)
    }],
    'qualification': [{  # Qualifications obtained by training and certification
        'identifier': ['-- Identifier --'],  # An identifier for this qualification for the practitioner
        'code': '-- CodeableConcept --',  # R!  Coded representation of the qualification
        'period': '-- Period --',  # Period during which the qualification is valid
        'issuer': '-- Reference(Organization) --'  # Organization that regulates and issues the qualification
    }],
    'communication': ['-- CodeableConcept --']  # A language the practitioner is able to use in patient communication
}

fhir_health_care_service_reference = {
    'resourceType': 'HealthcareService',
    # from Resource: id, meta, implicitRules, and language
    # from DomainResource: text, contained, extension, and modifierExtension
    'identifier': ['-- Identifier --'],  # External identifiers for this item
    'providedBy': '-- Reference(Organization) --',  # Organization that provides this service
    'serviceCategory': '-- CodeableConcept --',  # Broad category of service being performed or delivered
    'serviceType': [{  # Specific service delivered or performed
        'type': '-- CodeableConcept --',  # R!  Type of service delivered or performed
        'specialty': ['-- CodeableConcept --']  # Specialties handled by the Service Site
    }],
    'location': '-- Reference(Location) --',  # R!  Location where service may be provided
    'serviceName': '<string>',  # Description of service as presented to a consumer while searching
    'comment': '<string>',  # Additional description and/or any specific issues not covered elsewhere
    'extraDetails': '<string>',  # Extra details about the service that can't be placed in the other fields
    'photo': '-- Attachment --',  # Facilitates quick identification of the service
    'telecom': ['-- ContactPoint --'],  # Contacts related to the healthcare service
    'coverageArea': ['-- Reference(Location) --'],  # Location(s) service is inteded for/available to
    'serviceProvisionCode': ['-- CodeableConcept --'],  # Conditions under which service is available/offered
    'eligibility': '-- CodeableConcept --',  # Specific eligibility requirements required to use the service
    'eligibilityNote': '<string>',  # Describes the eligibility conditions for the service
    'programName': ['<string>'],  # Program Names that categorize the service
    'characteristic': ['-- CodeableConcept --'],  # Collection of characteristics (attributes)
    'referralMethod': ['-- CodeableConcept --'],  # Ways that the service accepts referrals
    'publicKey': '<string>',  # PKI Public keys to support secure communications
    'appointmentRequired': '<boolean>',  # If an appointment is required for access to this service
    'availableTime': [{  # Times the Service Site is available
        'daysOfWeek': ['<code>'],  # mon | tue | wed | thu | fri | sat | sun
        'allDay': '<boolean>',  # Always available? e.g. 24 hour service
        'availableStartTime': '<time>',  # Opening time of day (ignored if allDay = true)
        'availableEndTime': '<time>'  # Closing time of day (ignored if allDay = true)
    }],
    'notAvailable': [{  # Not available during this time due to provided reason
        'description': '<string>',  # R!  Reason presented to the user explaining why time not available
        'during': '-- Period --'  # Service not availablefrom this date
    }],
    'availabilityExceptions': '<string>'  # Description of availability exceptions
}

fhir_attachement_reference = {
    # from Element: extension
    'contentType': '<code>',  # Mime type of the content, with charset etc.
    'language': '<code>',  # Human language of the content (BCP-47)
    'data': '<base64Binary>',  # Data inline, base64ed
    'url': '<uri>',  # Uri where the data can be found
    'size': '<unsignedInt>',  # Number of bytes of content (if url provided)
    'hash': '<base64Binary>',  # Hash of the data (sha-1, base64ed)
    'title': '<string>',  # Label to display in place of the data
    'creation': '<dateTime>'  # Date attachment was first created
}

fhir_location_reference = {
    'resourceType': 'Location',
    # from Resource: id, meta, implicitRules, and language
    # from DomainResource: text, contained, extension, and modifierExtension
    'identifier': ['-- Identifier --'],  # Unique code or number identifying the location to its users
    'status': '<code>',  # active | suspended | inactive
    'name': '<string>',  # Name of the location as used by humans
    'description': '<string>',  # Description of the location
    'mode': '<code>',  # instance | kind
    'type': '-- CodeableConcept --',  # Type of function performed
    'telecom': ['-- ContactPoint --'],  # Contact details of the location
    'address': '-- Address --',  # Physical location
    'physicalType': '-- CodeableConcept --',  # Physical form of the location
    'position': {  # The absolute geographic location
        'longitude': '<decimal>',  # R!  Longitude with WGS84 datum
        'latitude': '<decimal>',  # R!  Latitude with WGS84 datum
        'altitude': '<decimal>'  # Altitude with WGS84 datum
    },
    'managingOrganization': '-- Reference(Organization) --',  # Organization responsible for provisioning and upkeep
    'partOf': '-- Reference(Location) --'  # Another Location this one is physically part of
}

fhir_related_person = {
    'resourceType': 'RelatedPerson',
    # from Resource: id, meta, implicitRules, and language
    # from DomainResource: text, contained, extension, and modifierExtension
    'identifier': ['-- Identifier --'],  # A human identifier for this person
    'patient': '-- Reference(Patient) --',  # R!  The patient this person is related to
    'relationship': '-- CodeableConcept --',  # The nature of the relationship
    'name': '-- HumanName --',  # A name associated with the person
    'telecom': ['-- ContactPoint --'],  # A contact detail for the person
    'gender': '<code>',  # male | female | other | unknown
    'birthDate': '<date>',  # The date on which the related person was born
    'address': ['-- Address --'],  # Address where the related person can be contacted or visited
    'photo': ['-- Attachment --'],  # Image of the person
    'period': '-- Period --'  # Period of time that this relationship is considered valid
}

fhir_medication_reference = {
    'resourceType': 'Medication',
    # from Resource: id, meta, implicitRules, and language
    # from DomainResource: text, contained, extension, and modifierExtension
    'code': '-- CodeableConcept --',  # Codes that identify this medication
    'isBrand': '<boolean>',  # True if a brand
    'manufacturer': '-- Reference(Organization) --',  # Manufacturer of the item
    'product': {  # Administrable medication details
        'form': '-- CodeableConcept --',  # powder | tablets | carton +
        'ingredient': [{  # Active or inactive ingredient
            'item': '-- Reference(Substance|Medication) --',  # R!  The product contained
            'amount': '-- Ratio --'  # Quantity of ingredient present
        }],
        'batch': [{  #
            'lotNumber': '<string>',  #
            'expirationDate': '<dateTime>'  #
        }]
    },
    'package': {  # Details about packaged medications
        'container': '-- CodeableConcept --',  # E.g. box, vial, blister-pack
        'content': [{  # What is  in the package
            'item': '-- Reference(Medication) --',  # R!  A product in the package
            'amount': '-- Quantity(SimpleQuantity) --'  # Quantity present in the package
        }]
    }
}

fhir_substance_reference = {
    'resourceType': 'Substance',
    # from Resource: id, meta, implicitRules, and language
    # from DomainResource: text, contained, extension, and modifierExtension
    'identifier': ['-- Identifier --'],  # Unique identifier
    'category': ['-- CodeableConcept --'],  # What class/type of substance this is
    'code': '-- CodeableConcept --',  # R!  What substance this is
    'description': '<string>',  # Textual description of the substance, comments
    'instance': [{  # If this describes a specific package/container of the substance
        'identifier': '-- Identifier --',  # Identifier of the package/container
        'expiry': '<dateTime>',  # When no longer valid to use
        'quantity': '-- Quantity(SimpleQuantity) --'  # Amount of substance in the package
    }],
    'ingredient': [{  # Composition information about the substance
        'quantity': '-- Ratio --',  # Optional amount (concentration)
        'substance': '-- Reference(Substance) --'  # R!  A component of the substance
    }]
}

fhir_ration_reference = {
    # from Element: extension
    'numerator': '-- Quantity --',  # Numerator value
    'denominator': '-- Quantity --'  # Denominator value
}

fhir_encounter_reference = {
    'resourceType': 'Encounter',
    # from Resource: id, meta, implicitRules, and language
    # from DomainResource: text, contained, extension, and modifierExtension
    'identifier': ['-- Identifier --'],  # Identifier(s) by which this encounter is known
    'status': '<code>',  # R!  planned | arrived | in-progress | onleave | finished | cancelled
    'statusHistory': [{  # List of past encounter statuses
        'status': '<code>',  # R!  planned | arrived | in-progress | onleave | finished | cancelled
        'period': '-- Period --'  # R!  The time that the episode was in the specified status
    }],
    'class': '<code>',  # inpatient | outpatient | ambulatory | emergency +
    'type': ['-- CodeableConcept --'],  # Specific type of encounter
    'priority': '-- CodeableConcept --',  # Indicates the urgency of the encounter
    'patient': '-- Reference(Patient) --',  # The patient present at the encounter
    'episodeOfCare': ['-- Reference(EpisodeOfCare) --'],
    # Episode(s) of care that this encounter should be recorded against
    'incomingReferral': ['-- Reference(ReferralRequest) --'],  # The ReferralRequest that initiated this encounter
    'participant': [{  # List of participants involved in the encounter
        'type': ['-- CodeableConcept --'],  # Role of participant in encounter
        'period': '-- Period --',  # Period of time during the encounter participant was present
        'individual': '-- Reference(Practitioner|RelatedPerson) --'
        # Persons involved in the encounter other than the patient
    }],
    'appointment': '-- Reference(Appointment) --',  # The appointment that scheduled this encounter
    'period': '-- Period --',  # The start and end time of the encounter
    'length': '-- Quantity(Duration) --',  # Quantity of time the encounter lasted (less time absent)
    'reason': ['-- CodeableConcept --'],  # Reason the encounter takes place (code)
    'indication': ['-- Reference(Condition|Procedure) --'],  # Reason the encounter takes place (resource)
    'hospitalization': {  # Details about the admission to a healthcare service
        'preAdmissionIdentifier': '-- Identifier --',  # Pre-admission identifier
        'origin': '-- Reference(Location) --',  # The location from which the patient came before admission
        'admitSource': '-- CodeableConcept --',  # From where patient was admitted (physician referral, transfer)
        'admittingDiagnosis': ['-- Reference(Condition) --'],
        # The admitting diagnosis as reported by admitting practitioner
        'reAdmission': '-- CodeableConcept --',
        # The type of hospital re-admission that has occurred (if any). If the value is absent, then this is not identified as a readmission
        'dietPreference': ['-- CodeableConcept --'],  # Diet preferences reported by the patient
        'specialCourtesy': ['-- CodeableConcept --'],  # Special courtesies (VIP, board member)
        'specialArrangement': ['-- CodeableConcept --'],  # Wheelchair, translator, stretcher, etc.
        'destination': '-- Reference(Location) --',  # Location to which the patient is discharged
        'dischargeDisposition': '-- CodeableConcept --',  # Category or kind of location after discharge
        'dischargeDiagnosis': ['-- Reference(Condition) --']
        # The final diagnosis given a patient before release from the hospital after all testing, surgery, and workup are complete
    },
    'location': [{  # List of locations where the patient has been
        'location': '-- Reference(Location) --',  # R!  Location the encounter takes place
        'status': '<code>',  # planned | active | reserved | completed
        'period': '-- Period --'  # Time period during which the patient was present at the location
    }],
    'serviceProvider': '-- Reference(Organization) --',  # The custodian organization of this Encounter record
    'partOf': '-- Reference(Encounter) --'  # Another Encounter this encounter is part of
}

fhir_episode_of_care_reference = {
    "resourceType": "EpisodeOfCare",
    # from Resource: id, meta, implicitRules, and language
    # from DomainResource: text, contained, extension, and modifierExtension
    "identifier": ['-- Identifier --'],  # Identifier(s) for the EpisodeOfCare
    "status": "<code>",  # R!  planned | waitlist | active | onhold | finished | cancelled
    "statusHistory": [{  # Past list of status codes
        "status": "<code>",  # R!  planned | waitlist | active | onhold | finished | cancelled
        "period": '-- Period --'  # R!  Period for the status
    }],
    "type": ['-- CodeableConcept --'],  # Type/class  - e.g. specialist referral, disease management
    "condition": ['-- Reference(Condition) --'],  # Conditions/problems/diagnoses this episode of care is for
    "patient": '-- Reference(Patient) --',  # R!  Patient for this episode of care
    "managingOrganization": '-- Reference(Organization) --',  # Organization that assumes care
    "period": '-- Period --',  # Interval during responsibility is assumed
    "referralRequest": ['-- Reference(ReferralRequest) --'],  # Originating Referral Request(s)
    "careManager": '-- Reference(Practitioner) --',  # Care manager/care co-ordinator for the patient
    "careTeam": [{  # Other practitioners facilitating this episode of care
        "role": ['-- CodeableConcept --'],  # Role taken by this team member
        "period": '-- Period --',  # Period of time for this role
        "member": '-- Reference(Practitioner|Organization) --'  # The practitioner (or Organization) within the team
    }]
}


