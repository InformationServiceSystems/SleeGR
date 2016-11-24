import csv
import pickle
import os

from dateutil import rrule
from datetime import datetime
from datetime import timedelta
from typing import Dict, List, Optional

from matplotlib.dates import hours

from linear_datascience import Comp1D
from datawrapper.value_wrapper import ValueWrapper
import numpy
import database



class DataReader:
    def __init__(self):
        '''
        CSV reader, to get healt data stored in csv
        :param date: format: datetime
        :param user_id: int
        '''
        self._db_inserts, self._db_extended = database.init()

    def read_data(self, user_id: str, start_date: datetime, end_date: datetime, measurement_type) -> Dict:
        ret_json = {}

        for day in rrule.rrule(rrule.DAILY, dtstart=start_date,
                               until=end_date):

            for row in self._db_extended.find_data(user_id, day, measurement_type):
                if measurement_to_valuenumb[
                    int(row['type'])] == 1:
                    ret_json[row['time_stamp']] = {
                        'value': row['val1']}
                elif measurement_to_valuenumb[
                    int(row.type)] == 2:
                    ret_json[row.time_stamp] = {
                        'value': {'value_1': row.val1,
                                  'value_2': row.val2}}
                elif measurement_to_valuenumb[
                    int(row.type)] == 3:
                    ret_json[row.time_stamp] = {
                        'value': {'value_1': row.val1,
                                  'value_2': row.val2,
                                  'value_3': row.val3}}
        return ret_json

    def read_sleep_data(self, user_id: str, start_date: datetime, end_date: datetime) -> List[Dict]:
        ret_list = []
        dates = []
        data = []
        cursors = self._db_extended.find_data_no_date(user_id, 777)
        for day in rrule.rrule(rrule.DAILY, dtstart=start_date,
                               until=end_date):
            dates.append(day.strftime('%d.%m.%Y'))
        for cursor in cursors:
            if cursor.time_stamp.strftime('%d.%m.%Y') in dates:
                data.append(cursor)

        for row in data:
            wake_up = row.time_stamp
            drop_off = row.val1
            duration = wake_up - drop_off
            deep_sleep = float(row.val2) * 100
            if deep_sleep > 0:
                ret_list.append(
                    {'user_id': user_id, 'date': (wake_up.strftime('%d.%m.%Y')),
                     'x': float(duration.seconds / 3600),
                     'y': deep_sleep})
        return ret_list

    def heart_rate_special(self, user_id: str, start_date:datetime, end_date: datetime) -> List[Dict]:
        ret_list = []
        dates = []
        cursors = list(self._db_extended.find_correl_data(user_id))
        hr_cursors = list(self._db_extended.find_data_tag(user_id, 21, 'Cooldown'))
        hr_cursors_rec = list(self._db_extended.find_data_tag(user_id, 21, 'Recovery'))
        hr_cursors.extend(hr_cursors_rec)
        hr_cursors = hr_cursors[::10]
        for day in rrule.rrule(rrule.DAILY, dtstart=start_date,
                               until=end_date):
            dates.append(day.strftime('%d.%m.%Y'))
        for day in dates:
            data = list(filter(lambda entry : entry.time_stamp().strftime('%d.%m.%Y') == day, cursors))
            if len(data) > 0:
                data = data[0]
                new_json = {}
                new_json['user_id'] = user_id
                new_json['date'] = day
                new_json['a'] = data.a()
                new_json['t'] = data.t()
                new_json['c'] = data.c()
                hr_lst_current_day = list(filter(lambda entry: entry.time_stamp.strftime('%d.%m.%Y') == day, hr_cursors))
                if len(hr_lst_current_day) < 1:
                    continue
                base_time = hr_lst_current_day[0].time_stamp
                datapoints = []
                for data in hr_lst_current_day:
                    datapoints.append({'x': (data.time_stamp - base_time).seconds, 'y': data.val0})
                new_json['data_points'] = datapoints
                new_json['rmse'] = self.calculate_rmse(new_json['data_points'], new_json['a'], new_json['t'], new_json['c'])
                ret_list.append(new_json)
        return ret_list

    def calculate_rmse(self, datapoints, a, t, c):
        ret_value = 0
        if a and t and c:
            for data in datapoints:
                function_value = (180-c)*math.exp(-(data['x']-t)/a)+c
                ret_value = ret_value + math.pow(function_value-data['y'],2)
            ret_value = math.sqrt(ret_value/len(datapoints))
            return ret_value
        else:
            return None

    def read_correlation_data(self, user_id: str, x_label: str, y_label: str, next_day: bool) -> Dict:
        data_cursor = self._db_extended.find_correl_data(user_id)
        data = []
        if len(data_cursor) == 0:
            return None
        if x_label == 'Sleep start':
            for d in data_cursor:
                data.append(d)
            reply = Comp1D(data, x_label, y_label, regr=True, B_next_day=False)
            if not reply:
                return None
            for key, val in reply.items():
                if type(val) == numpy.float64:
                    reply[key] = float(val)
                elif type(val) == list:
                    pass
                elif type(val) == numpy.int64:
                    reply[key] = int(val)
                elif type(val) == numpy.int32:
                    reply[key] = int(val)
            reply['x0'] = self.get_timedelta(reply['x0'])
            reply['x1'] = self.get_timedelta(reply['x1'])
            for data in reply['data']:
                data[0] = self.get_timedelta(data[0])
            return reply
        else:
            for d in data_cursor:
                data.append(d)
            reply = Comp1D(data, x_label, y_label, regr=True, B_next_day=False)
            if not reply:
                return None
            for key, val in reply.items():
                if type(val) == numpy.float64:
                    reply[key] = float(val)
                elif type(val) == list:
                    pass
                elif type(val) == numpy.int32:
                    reply[key] = int(val)
                elif type(val) == numpy.int64:
                    reply[key] = int(val)
            return reply

    def convert_from_numpy(self, value):
        if type(value) == numpy.float64:
            return float(value)
        elif type(value) == list:
            pass
        elif type(value) == numpy.int64:
            return int(value)

    def get_timedelta(self, value):
        midnight = datetime(year=2016, month=12, day=2, hour=0, minute=0, second= 0)
        time = timedelta(minutes=60 * value)
        time = midnight + time
        delta =time - datetime(year=2016, month=12, day=1, hour=0, minute=0, second= 0)
        return delta.total_seconds()


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
    s = DataReader()
    s.get_timedelta(-1.0)
