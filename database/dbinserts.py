import names
from database.database import DbBase
from databasemodels.models import User
import datawrapper.correl_wrapper as cw
import datawrapper.measure_wrapper as mw
import datawrapper.value_wrapper as vw

class DbInserts:
    def __init__(self, database):
        self.db_base = database

    def insert_user(self, user):
        """
        Insert a user into collection general_user.
        :param user: Need to be instance of User (see models.py)
        """
        self.db_base._general_users_collection.insert_one(user.encode())

    def insert_fitness_user(self, fitness_user):
        """
        Insert a fitness_user into collection fitness_user
        :param fitness_user: instance of FitnessUser
        """
        self.db_base._fitness_users_collection.insert_one(fitness_user.encode())

    def insert_service(self, service):
        """
        Insert a service into collection general_service
        :param service: instance of Service
        """
        self.db_base._service_collection.insert_one(service.encode())

    def insert_trainer(self, trainer):
        """
        Insert a trainer into collection trainer_user
        :param trainer: instance of Trainer
        """
        self.db_base._trainer_collection.insert_one(trainer.encode())

    def insert_service_user_map(self,service):
        """
        Insert a service into collection service_user_map
        :param service: Instance of of ServiceUserMap
        """
        self.db_base._user_map_collection.insert_one(service.encode())

    def find_user(self, email):
        asked_user_json = self.db_base._general_users_collection.find_one({names.email: email})
        if asked_user_json:
            return User.decode(asked_user_json)
        else:
            return None

    # def insert_heart_rate_data(self, json):
    #     self.db_base._db['heart_rate'].insert_one(json)

    # def insert_sleep_data(self, json):
    #     self.db_base._db['sleep_data'].insert_one(json)

    # def inser_fitness_data(self, measurement_type, json):
    #     self.db_base._db[str(measurement_type)].insert_one(json)

    def insert_fitness(self, user, json):
        """
        Deprecated
        :param user:
        :param json:
        :return:
        """
        self.db_base._db[user].insert_one(json)

    # newer

    def insert_value(self, user, value_wrapper):
        return self.db_base._db[user].insert_one(value_wrapper._value_json)

    def insert_csv_row(self, user, value_wrapper):
        if not self.insert_value(user, value_wrapper) is None:
            return True
        return False

    def insert_csv_row_many(self, user, value_wrapper_list):
        json_list = [value_json._value_json for value_json in value_wrapper_list]
        if not self.db_base._db[user].insert_many(json_list) is None:
            return True
        return False

    def insert_correl(self, user, correl_wrapper):
        self.db_base['%s_data' % (user)].insert(correl_wrapper._correlation_json)

    def insert_measure(self, measure_wrapper):
        ids = []
        user = ''
        for value in measure_wrapper:
            user = value.email
            ids.append(self.insert_value(value.email, value).inserted_id)
        measure_json = dict(measure_wrapper._measuremet_json)
        measure_json['value_ids'] = ids
        return self.db_base._db[('%s_measure' % user)].insert_one(measure_json)