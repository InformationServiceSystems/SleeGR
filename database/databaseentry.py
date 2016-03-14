from pymongo import MongoClient

from databasemodels.models import User, FitnessUser, Service, Trainer, ServiceUserMap


class DataBaseEntry:

    def __init__(self):
        _server_name = 'localhost'
        _mongodb_port = 27017
        self._client = MongoClient(_server_name, _mongodb_port)
        self._db = self._client.triathlon
        self._general_users_collection = self._db.general_user
        self._fitness_users_collection = self._db.fitness_user
        self._service_collection = self._db.general_service
        self._trainer_collection = self._db.trainer_user
        self._user_map_collection = self._db.user_map_service

    def insert_user(self, user):
        """
        Insert a user into collection general_user.
        :param user: Need to be instance of User (see models.py)
        """
        self._general_users_collection.insert_one(user.encode())

    def insert_fitness_user(self, fitness_user):
        """
        Insert a fitness_user into collection fitness_user
        :param fitness_user: instance of FitnessUser
        """
        self._fitness_users_collection.insert_one(fitness_user.encode())

    def insert_service(self, service):
        """
        Insert a service into collection general_service
        :param service: instance of Service
        """
        self._service_collection.insert_one(service.encode())

    def insert_trainer(self, trainer):
        """
        Insert a trainer into collection trainer_user
        :param trainer: instance of Trainer
        """
        self._trainer_collection.insert_one(trainer.encode())

    def insert_service_user_map(self,service):
        """
        Insert a service into collection service_user_map
        :param service: Instance of of ServiceUserMap
        """
        self._user_map_collection.insert_one(service.encode)

    def find_user(self, email):
        asked_user_json = self._general_users_collection.find_one({"email": email})
        if asked_user_json:
            return User.decode(asked_user_json)
        else:
            return None

    def get_user_id(self, email):
        asked_user = self._general_users_collection.find_one({"email": email})
        if asked_user:
            return asked_user['_id']
        else:
            return None

    def get_service_id(self, service_name):
        asked_service = self._service_collection.find_one({'service_name' : service_name});
        if asked_service:
            return asked_service['_id']
        else:
            return None

    def password_matches_email(self, email, password):
        asked_user = self.find_user(email)
        if asked_user is not None:
            if asked_user['password'] == password:
                return True
        return False




if __name__ == "__main__":
    dbe = DataBaseEntry()
    user = User("mail@m-heerde.de", "1234", "Matthias", "Heerde")
    dbe.insert_user(user)
    fitness_user = FitnessUser("mail@m-heerde.de", "05.08.1990", 90, 176)
    dbe.insert_fitness_user(fitness_user)
    print ((dbe.get_user_id("mail@m-heerde.de")))
    print(dbe.find_user("mail@m-heerde.de"))
    dbe._fitness_users_collection.drop()