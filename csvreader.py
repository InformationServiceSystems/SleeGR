import csv
import json
from enum import Enum
from flask import jsonify
from dateutil import rrule
class csvReader:
    def __init__(self):
        '''
        CSV reader, to get healt data stored in csv
        :param date: format: datetime
        :param user_id: int
        '''
        self.folder_path = '/root/data'

    def read_data(self, user_id, start_date, end_date, measurement_type):
        ret_json = {}

        for day in rrule.rrule(rrule.DAILY, dtstart=start_date, until=end_date):
            try :
                file_name = ('%s/%s/%s-%s.csv' % (self.folder_path, user_id, day.strftime('%Y.%m.%d'), measurement_type))
                with open(file_name, newline='') as csv_file:
                    fieldnames = ['UserID', 'measurement_type', 'time_stamp', 'Type_of_activity', 'value_1', 'value_2', 'value_3']
                    csv_reader = csv.DictReader(csv_file, fieldnames=fieldnames)
                    for row in csv_reader:
                        if measurement_to_valuenumb[int(row['measurement_type'])] == 1:
                            ret_json[row['time_stamp']] = {'value' : row['value_1']}
                        elif measurement_to_valuenumb[int(row['measurement_type'])] == 2:
                            ret_json[row['time_stamp']] = {'value' : {'value_1': row['value_1'], 'value_2': row['value_2']}}
                        elif measurement_to_valuenumb[int(row['measurement_type'])] == 3:
                            ret_json[row['time_stamp']] = {'value' : {'value_1': row['value_1'], 'value_2': row['value_2'], 'value_3': row['value_3']}}
                        else:
                            ret_json[row['time_stamp']] = {'value' : {'value_1': row['value_1'], 'value_2': row['value_2'], 'value_3': row['value_3']}}

            except FileNotFoundError:
                pass
        return json.dumps(ret_json, sort_keys=True, indent=4)

"""
a = csvReader()
print(a.read_data(datetime.datetime(year=2016, day=5, month=2), datetime.datetime(year=2016, day=5, month=2), 1234,21))
"""
measurement_to_valuenumb = {
    21: 1,
    1: 3,
    512: 3,
    31: 3,
    32: 3,
    33: 1,
    34: 1,
    35: 1,
    36: 1,
    37: 1,
    38: 1,
    13: 3
}
