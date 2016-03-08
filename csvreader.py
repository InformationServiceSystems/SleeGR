import csv
import datetime
import json

from flask import jsonify
from dateutil import rrule
class csvReader:
    def __init__(self):
        '''
        CSV reader, to get healt data stored in csv
        :param date: format: datetime
        :param user_id: int
        '''
        self.folder_path = '/home/matthias/Dokumente/UdS/iss/channels_data_example'

    def read_data(self, start_date, end_date, user_id, measurement_type):
        ret_json = {}

        for day in rrule.rrule(rrule.DAILY, dtstart=start_date, until=end_date):
            try :
                with open('%s/%s/%s-%s.csv' % (self.folder_path, str(user_id), day.strftime('%Y.%m.%d'), str(measurement_type)), newline='') as csv_file:
                    fieldnames = ['measurement_type', 'user_id', 'datetime', 'value_type', 'value1', 'value2', 'value3']
                    csv_reader = csv.DictReader(csv_file, fieldnames=fieldnames)
                    for row in csv_reader:

                        ret_json[row['datetime']] = {'value1' : row['value1'], 'value2' : row['value2'], 'value3' : row['value3']}
            except FileNotFoundError:
                pass
        return json.dumps(ret_json, sort_keys=True, indent=4)


a = csvReader()
print(a.read_data(datetime.datetime(year=2016, day=5, month=2), datetime.datetime(year=2016, day=5, month=2), 1234,21))

