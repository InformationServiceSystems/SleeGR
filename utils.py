import jwt
from dotenv import load_dotenv
import os
import base64
import requests
from flask import json
from datetime import datetime
from typing import Optional, Dict, List, Union



env = os.environ

client_id = env['AUTH0_CLIENT_ID']
client_secret = env['AUTH0_CLIENT_SECRET']

try:
    proxy = env['PROXY']
except KeyError:
    proxy=None

proxyDict = {
    'http': proxy,
    'https': proxy,
    'ftp': proxy
}

def get_user_info(auth):
    parts = auth.split()
    token = parts[1]
    payload = jwt.decode(
        token,
        base64.b64decode(client_secret.replace("_", "/").replace("-", "+")),
        audience=client_id
    )
    token_url = "https://{domain}/api/v2/users/{user_id}".format(domain=env['AUTH0_DOMAIN'], user_id=payload['sub'])
    data = {
        'include_fields':'false'
    }

    json_header = {
        'authorization' : 'Bearer ' + env['AUTH0_KEY'],
        'content-type': 'application/json'
    }
    user = requests.get(token_url, params=json.dumps(data), headers=json_header, proxies=proxyDict).json()

    return user

def iso_date2str(date_string):
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

def transform_tiny_to_FHIR(dict):
    try:
        tag = dict['type'] + ' Tracking'
        type = dict['type']
        user = dict['userID']
        device = dict['deviceID']
        timestamp = iso_date2str(dict['timestamp'])
        unit = dict['unit']
        components = []
        for key in dict['values'].keys():
            components.append({'code': key, 'value': dict['values'][key]})
    except KeyError:
        return None

    measure_scheme = {
			"category" : {
					"coding" : [
							{
									"display" : tag
							}
					]
			},
			"subject" : {
					"display" : user
			},
			"status" : "final",
			"device" : {
					"display" : device,
					"reference" : "http://iot01.iss.uni-saarland.de:81/get_device_code"
			},
			"component" : [],
			"effectiveDateTime" : timestamp
		}
    for val in components:
        component_scheme = {
            "valueDateTime" : timestamp,
            "code" : {
                    "coding" : [
                            {
                                    "display" : type,
                                    "system" : "http://loinc.org",
                                    "code" : "8867-4"
                            }
                    ]
            },
            "valueQuantity" : {
                    "system" : "http://unitsofmeasure.org",
                    "code" : val['code'],
                    "value" : val['value'],
                    "unit" : unit
            }
        }
        measure_scheme['component'].append(component_scheme)
    return measure_scheme
