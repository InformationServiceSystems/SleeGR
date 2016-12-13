from database.database import DbBase
import names
import pymongo
from typing import List, Optional
from datetime import datetime, timedelta
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


    def find_data_tag(self, user: str, measurement: str, tag=None) -> List[Optional[value_wrapper.ValueWrapper]]:
        res_lst = self.db_base._db[('%s_measure' % user)].find({'category.coding.display': tag})
        res_lst = list(res_lst)
        measure_list = []
        for elem in res_lst:
            elem = dict(elem)
            ids = elem['value_ids']
            values = []
            for value_id in ids:
                value_list = []
                if tag:
                    value_list = self.db_base._db[user].find({'_id': value_id, 'code.coding.display': measurement})
                else:
                    value_list = self.db_base._db[user].find({'_id': value_id})
                for value in value_list:
                    del value['_id']
                    values.append(dict(value))
            del elem['_id']
            del elem['value_ids']
            elem['component'] = values
            measure_list.append(measure_wrapper.measure_wrapper(elem))
        return_list = []
        for measurement in measure_list:
            for value in measurement:
                return_list.append(value)
        return return_list

    #changed to wrapper, not checked
    def find_data_user(self, user: str) -> List[Optional[value_wrapper.ValueWrapper]]:
        res_lst = self.db_base._db[('%s_measure' % user)].find()
        measure_list = []
        for elem in res_lst:
            elem = dict(elem)
            ids = elem['value_ids']
            values = []
            for value_id in ids:
                for value in self.db_base._db[user].find({'_id': value_id}):
                    del value['_id']
                    values.append(dict(value))
            del elem['_id']
            del elem['value_ids']
            elem['component'] = values
            temp = measure_wrapper.measure_wrapper(elem)
            if not temp:
                continue
            measure_list.append(measure_wrapper.measure_wrapper(elem))
        return_list = []
        for measurement in measure_list:
            for value in measurement:
                return_list.append(value)
        return return_list

    # changed to wrapper, not checked
    def find_data(self, user: str, time_stamp: datetime, measurement:str) -> List[Optional[value_wrapper.ValueWrapper]]:
            min_date = time_stamp
            max_date = min_date + timedelta(1)
            res_lst = self.db_base._db[('%s_measure' % user)].find({'effectiveDateTime': {'$lte': max_date, '$gte': min_date}})
            measure_list = []
            for elem in res_lst:
                elem = dict(elem)
                ids = elem['value_ids']
                values = []
                for value_id in ids:
                    for value in self.db_base._db[user].find({'_id': value_id, 'category.coding.display': measurement}):
                        del value['_id']
                        values.append(dict(value))
                del elem['_id']
                del elem['value_ids']
                elem['component'] = values
                measure_list.append(measure_wrapper.measure_wrapper(elem))
            return_list = []
            for measurement in measure_list:
                for value in measurement:
                    return_list.append(value)
            return return_list

    # changed to wrapper, not checked
    def find_data_no_date(self, user, measurement)-> List[Optional[value_wrapper.ValueWrapper]]:
        res_lst = self.db_base._db[('%s_measure' % user)].find()
        measure_list = []
        for elem in res_lst:
            elem = dict(elem)
            ids = elem['value_ids']
            values = []
            for value_id in ids:
                for value in self.db_base._db[user].find({'_id': value_id, 'category.coding.display': measurement}):
                    del value['_id']
                    values.append(dict(value))
            del elem['_id']
            del elem['value_ids']
            elem['component'] = values
            measure_list.append(measure_wrapper.measure_wrapper(elem))
        return_list = []
        for measurement in measure_list:
            for value in measurement:
                return_list.append(value)
        return return_list

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

    def get_device_code(self, device_name=None):
        if device_name:
            return self.db_base._devices_db.devices_collection.find_one({'_id': device_name})
        else:
            return self.db_base._devices_db.devices_collection.find()

    def get_next_sequence(self, sequence_name):
        res = self.db_base._devices_db.counters.find_one_and_update({'_id':sequence_name}, {'$inc':{'seq': 1}})
        return res['seq']

