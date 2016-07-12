import os, glob
import csv
import re
from datetime import datetime
import database
import pprint

from dateutil import rrule


class csv_2_reader():

    def __init__(self):
        self.db_inserts, self.db_extended = database.init()
        self.folder_path = "/home/matthias/data"

    def to_mongo(self, user_id):
        lst = self.to_json(user_id)
        for json in lst:
            self.db_inserts.insert_csv_row(user_id, json)
        print('done')

    def to_json(self, user_id):
        ret_list = []
        folder = ('%s/%s' % (self.folder_path, user_id))
        for file_name in os.listdir(folder):
            try:
                with open(os.path.join(folder, file_name), newline='') as csv_file:
                    if re.search('sleep', file_name) is None:
                        fieldnames = ['UserID', 'measurement_type', 'time_stamp',
                                      'Type_of_activity', 'value_1', 'value_2',
                                      'value_3']
                        csv_reader = csv.DictReader(csv_file, fieldnames=fieldnames)
                        for row in csv_reader:
                            new_json = {'UserID': row['UserID'], 'type': int(row['measurement_type']),
                                        'time_stamp': datetime.strptime(row['time_stamp'], "%Y.%m.%d_%H:%M:%S"), 'tag': row['Type_of_activity'],
                                        'val0': float(row['value_1']), 'val1': float(row['value_1']), 'val2': float(row['value_3'])}
                            ret_list.append(new_json)
                    else:
                        csv_reader = csv.reader(csv_file)
                        is_value = False
                        value_list =[]
                        for row in csv_reader:
                            if is_value:
                                value_list.append(row)
                                is_value = False
                            else:
                                is_value = True
                        for value in value_list:
                            new_json = {}
                            new_json['type'] = 777
                            new_json['time_stamp'] = datetime.strptime(value[3], '%d. %m. %Y %H:%M')
                            new_json['tag'] = ''
                            new_json['val0'] = float(value[5])
                            new_json['val1'] = datetime.strptime(value[2], '%d. %m. %Y %H:%M')
                            new_json['val2'] = float(value[12])
                            ret_list.append(new_json)
            except Exception as e:
                print('messed up', file_name)
        return ret_list


def push_to_db():
    c2r = csv_2_reader()
    folder_path = "/home/matthias/data"
    for user in os.listdir(folder_path):
        print(user)
        c2r.to_mongo(user)

if __name__ == '__main__':
    push_to_db()

