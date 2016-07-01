import csv
import pickle
import os

from dateutil import rrule
from datetime import datetime

from linear_datascience import Comp1D
import json
import numpy
import database

from sleegr_reader import read_hr_data


class dataReader:
    def __init__(self):
        '''
        CSV reader, to get healt data stored in csv
        :param date: format: datetime
        :param user_id: int
        '''
        self._db_inserts, self._db_extended = database.init()
        self.folder_path = "/home/matthias/data"


    def read_data(self, user_id, start_date, end_date, measurement_type):
        ret_json = {}

        for day in rrule.rrule(rrule.DAILY, dtstart=start_date,
                               until=end_date):

            for row in self._db_extended.find_data(user_id, day, measurement_type):
                if measurement_to_valuenumb[
                    int(row['measurement_type'])] == 1:
                    ret_json[row['time_stamp']] = {
                        'value': row['value_1']}
                elif measurement_to_valuenumb[
                    int(row['measurement_type'])] == 2:
                    ret_json[row['time_stamp']] = {
                        'value': {'value_1': row['value_1'],
                                  'value_2': row['value_2']}}
                elif measurement_to_valuenumb[
                    int(row['measurement_type'])] == 3:
                    ret_json[row['time_stamp']] = {
                        'value': {'value_1': row['value_1'],
                                  'value_2': row['value_2'],
                                  'value_3': row['value_3']}}

        # return json.JSONEncoder().encode(ret_json)
        return ret_json

    def ReadSleepData(self, user_id, start_date, end_date):
        ret_list = []

        for day in rrule.rrule(rrule.DAILY, dtstart=start_date,
                               until=end_date):
            for row in self._db_extended.find_data(user_id, day):
                # avoid weirdness at the end of the file
                wake_up = datetime.strptime(row['time_stamp'], '%d. %m. %Y %H:%M')
                drop_off = datetime.strptime(row['val1'], '%d. %m. %Y %H:%M')
                duration = wake_up - drop_off
                deep_sleep = float(row['val2']) * 100
                if deep_sleep > 0:
                    ret_list.append(
                        {'user_id': user_id, 'date': (wake_up.date().strftime('%d.%m.%Y')),
                         'x': float(duration.seconds / 3600),
                         'y': deep_sleep})
        return ret_list

    def heart_rate_sepecial(self, user_id, start_date, end_date):
        print('in hr special')
        ret_list = []
        file_name = ('%s/%s/' % (self.folder_path, user_id))
        #data_name = ('%s/%s/%s.data' % (self.folder_path, user_id, user_id))

        #data_file = open(data_name, "r+b")
        #data_lst = pickle.load(data_file)
        data_lst = self._db_extended.find_correl_data(user_id)
        hr_cursor_lst = []
        hr_lst = []


        for day in rrule.rrule(rrule.DAILY, dtstart=start_date,
                               until=end_date):
            new_json = {}
            new_json['user_id'] = user_id
            new_json['date'] = day.strftime('%d.%m.%Y')
            for data in data_lst:
                if data['time_stamp'].date() == day.date():
                    new_json['a'] = data['A']
                    new_json['t'] = data['T']
                    new_json['c'] = data['C']
            hr_cursor_lst.append(self._db_extended.find_data(user_id, day, 21))
        for cursor in hr_cursor_lst:
            for data in cursor:
                print(data)
                hr_lst.append(data)
        hr_lst.sort(key=lambda date : datetime.strptime(date['time_stamp']), )
        return ret_list

    def read_correlation_data(self, user_id, x_label, y_label, next_day):
        #data_name = ('%s/%s/%s.data' % (self.folder_path, user_id, user_id))

        #data = pickle.load(open(data_name, "r+b"))

        data = self._db_extended.find_correl_data(user_id)

        to_reply = (x_label, y_label, next_day)
        reply = Comp1D(data, x_label, y_label, regr=True, B_next_day=False)
        for key, val in reply.items():
            if type(val) == numpy.float64:
                reply[key] = float(val)
                print(type(reply[key]))
            elif type(val) == list:
                pass
            elif type(val) == numpy.int64:
                reply[key] = int(val)


    # ... convert to json and send reply to the client page

        return reply





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
    13: 3,
    777: 1
}


if __name__ == '__main__':
    s = csvReader()
    s.to_mongo('test@test.com')