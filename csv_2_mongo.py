from datetime import datetime
import csvreader
import database
from database import init

from dateutil import rrule


class csv_2_reader():

    def __init__(self):
        self.db, self.dbe = database.init()

    def transfer_data(self, user, start_date, end_date, activity):
        csv_reader = csvreader.csvReader()
        if activity == 21:
            for day in rrule.rrule(rrule.DAILY, dtstart=start_date,
                                   until=end_date):
                current_json_list = csv_reader.heart_rate_sepecial(user, day, day)
                for j in current_json_list:
                    self.db.insert_fitness(user, j)

    def search_data(self, user, start_date, end_date, activity):
        pass


csv = csv_2_reader()
csv.transfer_data('test@test.com', datetime(2016, 1, 1), datetime(2016, 3, 31), 21)