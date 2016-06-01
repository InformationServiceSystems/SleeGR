import os, glob

from datetime import datetime
import csvreader
import database

from dateutil import rrule


class csv_2_reader():

    def __init__(self):
        self.db, self.dbe = database.init()

    def transfer_data(self, user, date, activity):
        csv_reader = csvreader.csvReader()
        if activity == 21:
            print('HI')
            print(date)
            current_json_list = csv_reader.heart_rate_sepecial(user, date, date)

            for j in current_json_list:
                print(j)
                self.db.insert_heart_rate_data(j)
        elif activity == 777:
            current_json_list = csv_reader.ReadSleepData(user, date, date)
            for j in current_json_list:
                self.db.insert_sleep_data(j)
        else:
            current_json_list = csv_reader.read_data(user, date, date, activity)
            for j in current_json_list:
                print('j ist:')
                print(type(j))
                j['user_id'] = user
                j['date'] = date
                self.db.inser_fitness_data(activity, j)

    def search_data_single(self, user, date, activity):
        csv_reader = csvreader.csvReader()
        if activity == 21:
            return self.dbe.find_heart_rate_data(date, user)

        elif activity == 777:
            return self.dbe.find_sleep_data(date, user)

        else:
            res_json = csv_reader.read_data(user, date, date, activity)
            del(res_json['user_id'])
            del(res_json['date'])
            return res_json

    def search_data_bulk(self, user, start_date, end_date, activity):
        ret_lst = []
        if activity == 21:
            for day in rrule.rrule(rrule.DAILY, dtstart=start_date,
                                   until=end_date):
                ret_lst.append(self.search_data_single(user, day, activity))


        elif activity == 777:
            for day in rrule.rrule(rrule.DAILY, dtstart=start_date,
                                   until=end_date):
                ret_lst.append(self.search_data_single(user, day, activity))
        else:
            for day in rrule.rrule(rrule.DAILY, dtstart=start_date,
                               until=end_date):
                ret_lst.append(self.search_data_single(user, day, activity))

        return ret_lst


if __name__ == '__main__':
    os.chdir("/home/matthias/data")
    user_folders = (os.listdir("/home/matthias/data"))
    translater = csv_2_reader()

    start_date = datetime(2016, 1, 1)
    end_date = datetime(2016, 6, 1)
    measures = csvreader.measurement_to_valuenumb.keys()
    for user_folder in user_folders:
        for day in rrule.rrule(rrule.DAILY, dtstart=start_date,
                           until=end_date):
            for measure in measures:
                translater.transfer_data(user_folder, day, measure)