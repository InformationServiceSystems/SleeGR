import csv
import json
from dateutil import rrule
from datetime import datetime


class csvReader:
    def __init__(self):
        '''
        CSV reader, to get healt data stored in csv
        :param date: format: datetime
        :param user_id: int
        '''
        #self.folder_path = "/home/matthias/Dokumente/UdS/iss/data"
        self.folder_path = "/root/data"

    def read_data(self, user_id, start_date, end_date, measurement_type):
        ret_json = {}

        for day in rrule.rrule(rrule.DAILY, dtstart=start_date, until=end_date):
            try:
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
        #return json.JSONEncoder().encode(ret_json)
        return ret_json

    def ReadSleepData(self, user_id, start_date, end_date):
        filename = ('%s/%s/sleep-export.csv' % (self.folder_path, user_id,))
        ret_list = []
        with open(filename, newline='') as csvfile:
            file_reader = csv.reader(csvfile, delimiter=',')
            self.sleepRawData = []
            for row in file_reader:
                # avoid weirdness at the end of the file
                if len(row) < 1:
                    continue
                if row[0] == 'Id':
                    continue
                wake_up = datetime.strptime(row[3],'%d. %m. %Y %H:%M')
                drop_off = datetime.strptime(row[2], '%d. %m. %Y %H:%M')
                wake_up.date()
                if wake_up.date() >= start_date.date() and wake_up.date() <= end_date.date():
                    duration = wake_up - drop_off
                    deep_sleep = float(row[12]) * 100
                    hours = int(duration.seconds) / 3600
                    ret_list.append({'user_id': user_id, 'date': str(wake_up.date()), 'x': float(duration.seconds / 3600), 'y': deep_sleep})
        return ret_list

    def heart_rate_sepecial(self,user_id, start_date, end_date):
        ret_list = []
        for day in rrule.rrule(rrule.DAILY, dtstart=start_date, until=end_date):
            heart_rate_json = self.read_data(user_id, day, day, '21')
            fkt_json = self.read_data(user_id, day, day, '32')
            if heart_rate_json is None:
                continue
            new_json = {}
            new_json['user_id'] = user_id
            new_json['date'] = day.strftime('%m/%d/%Y')
            if fkt_json is None:
                    new_json['a'] = 0
                    new_json['b'] = 0
                    new_json['c'] = 0
            else:
                for key in fkt_json:
                    new_json['a'] = fkt_json[key]['value']['value_1']
                    new_json['b'] = fkt_json[key]['value']['value_2']
                    new_json['c'] = fkt_json[key]['value']['value_3']
            datapoints = []
            counter = 0
            for measurement in heart_rate_json:
                if counter >= 300:
                    break
                datapoints.append({'x': counter, 'y':heart_rate_json[measurement]['value']})
                counter += 1
            new_json['datapoints'] = datapoints
            ret_list.append(new_json)
        return ret_list

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
"""
s = csvReader()
e = s.ReadSleepData('test@test.com', datetime(2016, 1,1), datetime(2016, 3, 31))
print(e)
"""