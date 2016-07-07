from database.database import DbBase
import names
from datetime import datetime

class DbExtended:
    def __init__(self, database):
        self.db_base = database


    def get_user_id(self, email):
        asked_user = self.db_base._general_users_collection.find_one({names.email: email})
        if asked_user:
            return asked_user['_id']
        else:
            return None

    def get_service_id(self, service_name):
        asked_service = self.db_base._service_collection.find_one({names.service_name : service_name});
        if asked_service:
            return asked_service['_id']
        else:
            return None

    def password_matches_email(self, email, password):
        asked_user_json = self.db_base._general_users_collection.find_one({names.email: email})
        if asked_user_json is not None:
            if asked_user_json[names.password] == password:
                return True
        return False

    def email_in_use(self, email):
        if self.db_base._general_users_collection.find_one({names.email: email}) is not None:
            return True
        return False

    def find_fitness_value(self, user, measurement_type, date):
        self.db_base._db[user].find_one()


#new
    def find_heart_rate_data(self, date, user):
        datum = date.strftime('%d.%m.%Y')
        return self.db_base._db['heart_rate'].find_one({'user_id': user, 'date': datum})

    def find_sleep_data(self, date, user):
        datum = date.strftime('%d.%m.%Y')
        return self.db_base._db['sleep_data'].find_one({'user_id': user, 'date': datum})

    def find_fitness_data(self, measurement_type, date, user):
        datum = date.strftime('%d.%m.%Y')
        return self.db_base._db[str(measurement_type)].find_one({'user_id': user, 'date': datum,
                                                          'type': measurement_type})

    def find_data_tag(self, user, measurement, tag=''):
        return self.db_base._db[user].find({'type': measurement, 'tag': tag})

    def find_data(self, user, time_stamp, measurement):
        ret_lst =[]
        for data in self.db_base._db[user].find({'type': measurement}):
            if data['time_stamp'].date() == time_stamp.date():
                ret_lst.append(data)
        return ret_lst

    def find_data_no_date(self, user, measurement):
        return self.db_base._db[user].find({'type': measurement})


    def find_correl_data(self, user):
        collection_name = ('%s_data' % user)
        return self.db_base._db[collection_name].find()

    def find_one_correl_data_date(self, user, time_stamp):
        tmp_lst = []
        for data in self.find_correl_data(user):
            if (data['time_stamp']).date() == time_stamp.date():
                tmp_lst.append(data)
        for data in tmp_lst:
            if data['A'] is not None:
                return data
        return None

