from datetime import datetime
import csvreader
import database
from database import init

from dateutil import rrule


class csv_2_reader():

    def __init__(self):
        self.db, self.dbe = database.init()

    def transfer_data(self, user, date, activity):
        csv_reader = csvreader.csvReader()
        if activity == 21:
            current_json_list = csv_reader.heart_rate_sepecial(user, date, date)
            for j in current_json_list:
                self.db.insert_heart_rate_data(j)
        elif activity == 777:
            current_json_list = csv_reader.ReadSleepData(user, date, date)
            for j in current_json_list:
                self.db.insert_sleep_data(j)
        else:
            current_json_list = csv_reader.read_data(user, date, date, activity)
            for j in current_json_list:
                j['user_id'] = user
                j['date'] = date
                self.db.inser_fitness_data(activity, j)

    def search_data(self, user, start_date, end_date, activity):
        pass


csv = csv_2_reader()
csv.transfer_data('test@test.com', datetime(2016, 1, 1), 21)