import csv
from dateutil import rrule
from datetime import datetime


from sleegr_reader import read_hr_data


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

        for day in rrule.rrule(rrule.DAILY, dtstart=start_date,
                               until=end_date):
            try:
                file_name = ('%s/%s/%s-%s.csv' % (
                self.folder_path, user_id, day.strftime('%Y.%m.%d'),
                measurement_type))
                with open(file_name, newline='') as csv_file:
                    fieldnames = ['UserID', 'measurement_type', 'time_stamp',
                                  'Type_of_activity', 'value_1', 'value_2',
                                  'value_3']
                    csv_reader = csv.DictReader(csv_file,
                                                fieldnames=fieldnames)
                    for row in csv_reader:
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
                        else:
                            ret_json[row['time_stamp']] = {
                                'value': {'value_1': row['value_1'],
                                          'value_2': row['value_2'],
                                          'value_3': row['value_3']}}

            except FileNotFoundError:
                pass
        # return json.JSONEncoder().encode(ret_json)
        return ret_json

    def ReadSleepData(self, user_id, start_date, end_date):
        filename = ('%s/%s/sleep-export.csv' % (self.folder_path, user_id,))
        print(filename)
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
                wake_up = datetime.strptime(row[3], '%d. %m. %Y %H:%M')
                drop_off = datetime.strptime(row[2], '%d. %m. %Y %H:%M')
                wake_up.date()
                if wake_up.date() >= start_date.date():
                    if wake_up.date() <= end_date.date():
                        duration = wake_up - drop_off
                        deep_sleep = float(row[12]) * 100
                        if deep_sleep > 0:
                            ret_list.append(
                            {'user_id': user_id, 'date': (wake_up.date().strftime('%d.%m.%Y')),
                             'x': float(duration.seconds / 3600),
                             'y': deep_sleep})
        return ret_list

    def heart_rate_sepecial(self, user_id, start_date, end_date):
        ret_list = []
        file_name = ('%s/%s/' % (
                self.folder_path, user_id))
        for day in rrule.rrule(rrule.DAILY, dtstart=start_date,
                               until=end_date):
            tpl_lst = read_hr_data(file_name, day)
            fkt_json = self.read_data(user_id, day, day, '32')
            if  not tpl_lst:
                continue
            new_json = {}
            new_json['user_id'] = user_id
            new_json['date'] = day.strftime('%d.%m.%Y')
            #if fkt_json is None:
            new_json['a'] = 1
            new_json['b'] = 1
            new_json['c'] = 1
            for key in fkt_json:
                new_json['a'] = float(fkt_json[key]['value']['value_1'])
                new_json['b'] = float(fkt_json[key]['value']['value_2'])
                new_json['c'] = float(fkt_json[key]['value']['value_3'])
            datapoints = []
            counter = 0
            for measurement in tpl_lst:
                #if counter % 10 < 0:
                #     continue
                datapoints.append({'x': measurement[0],
                                   'y':measurement[1]})
            new_json['data_points'] = datapoints
            if not datapoints:
                pass
            else:
                ret_list.append(new_json)
        return ret_list



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


if __name__ == '__main__':
    s = csvReader()
    e = s.heart_rate_sepecial('test@test.com', datetime(2016, 1, 1),
                              datetime(2016, 3, 31))
    for ee in e:
        print(ee)
