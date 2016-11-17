from database.database import DbBase
import names
import pymongo
from typing import List, Optional
from datetime import datetime
import bcrypt
from datawrapper import correl_wrapper, measure_wrapper, value_wrapper

class DbExtended:
    def __init__(self, database):
        self.db_base = database

    def get_all_users(self):
        asked_users = self.db_base._general_users_collection.find()
        if asked_users:
            return asked_users
        else:
            return None

    def drop_correl(self, user: str):
        self.db_base._db.drop_collection('%s_data' % user)

    def get_user_id(self, email: str):
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
            if bcrypt.hashpw(password.encode(), asked_user_json[names.password] )== asked_user_json[names.password]:
                return True
        return False

    def email_in_use(self, email):
        if self.db_base._general_users_collection.find_one({names.email: email}) is not None:
            return True
        return False

    def find_fitness_value(self, user, measurement_type, date):
        self.db_base._db[user].find_one()


#new
    # def find_heart_rate_data(self, date, user):
    #     datum = date.strftime('%d.%m.%Y')
    #     return correl_wrapper.correl_wrapper_gen(self.db_base._db['heart_rate'].find_one({'user_id': user, 'date': datum}))

    # def find_sleep_data(self, date, user):
    #     datum = date.strftime('%d.%m.%Y')
    #     return correl_wrapper.correl_wrapper_gen(self.db_base._db['sleep_data'].find_one({'user_id': user, 'date': datum}))

    # def find_fitness_data(self, measurement_type, date, user):
    #     datum = date.strftime('%d.%m.%Y')
    #     return correl_wrapper.correl_wrapper_gen(self.db_base._db[str(measurement_type)].find_one({'user_id': user, 'date': datum,
    #                                                       'type': measurement_type}))

    #changed to wrapper, not checked
    #TODO: type for tag
    def find_data_tag(self, user: str, measurement: str, tag ='') -> List[Optional[value_wrapper.ValueWrapper]]:
        res_lst = self.db_base._db[user].find({'type': measurement, 'tag': tag}).sort('time_stamp', pymongo.ASCENDING)
        ret_lst = []
        for elem in res_lst:
            del elem['_id']
            ret_lst.append(value_wrapper.value_wrapper(elem))
        return ret_lst

    #changed to wrapper, not checked
    def find_data_user(self, user:str) -> List[Optional[value_wrapper.ValueWrapper]]:
        res_lst = self.db_base._db[user].find()#.sort('time_stamp', pymongo.ASCENDING)
        ret_lst = []
        for elem in res_lst:
            del elem['_id']
            ret_lst.append(value_wrapper.value_wrapper(elem))
        return ret_lst

    # changed to wrapper, not checked
    def find_data(self, user:str , time_stamp:datetime, measurement:str) -> List[Optional[value_wrapper.ValueWrapper]]:
        ret_lst =[]
        for elem in self.db_base._db[user].find({'type': measurement}):
            if elem['time_stamp'].date() == time_stamp.date():
                del elem['_id']
                ret_lst.append(value_wrapper.value_wrapper(elem))
        return ret_lst

    # changed to wrapper, not checked
    def find_data_no_date(self, user, measurement)-> List[Optional[value_wrapper.ValueWrapper]]:
        ret_lst = []
        for elem in self.db_base._db[user].find({'type': measurement}):
            del elem['_id']
            ret_lst.append(value_wrapper.value_wrapper(elem))
        return ret_lst

    # changed to wrapper, not checked
    def find_correl_data(self, user: str) -> List[correl_wrapper.CorrelWrapper]:
        collection_name = ('%s_data' % user)
        jsons = self.db_base._db[collection_name].find()
        ret_lst = []
        for elem in self.db_base._db[collection_name].find():
            if elem:
                del elem['_id']
                ret_lst.append(correl_wrapper.correl_wrapper_gen(elem))
        return ret_lst

    # changed to wrapper, not checked
    # def find_one_correl_data_date(self, user: str, time_stamp: datetime)-> Optional[List[correl_wrapper.Correlwrapper]]:
    #     tmp_lst = []
    #     for data in self.find_correl_data(user):
    #         if data.time_stamp == time_stamp.date():
    #             tmp_lst.append(data)
    #     for data in tmp_lst:
    #         #TODO: THINK ABOUT THIS IF
    #         if data.a is not None:
    #             return data
    #     return None

