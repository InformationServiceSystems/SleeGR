from pymongo import MongoClient

from database.models import User, FitnessUser, Service, Trainer


class DataBaseEntry:

    def __init__(self):
        _server_name = 'localhost'
        _mongodb_port = 27017
        self._client = MongoClient(_server_name, _mongodb_port)
        self._db = self._client.triathlon
        self._general_users_collection = self._db.user
        self._fitness_users_collection = self._db.fitness_user
        self._service_collection = self._db.service
        self._trainer_collection = self._db.trainer

    def insert_user(self, user):
        """
        Insert a user in the user collection.
        :param user: Need to be instance of User (see models.py)
        """
        self._general_users_collection.insert_one(user.encode())

    def find_user(self, email):
        asked_user = self._general_users_collection.find_one({"email": email})
        if asked_user:
            return user.decode(asked_user)
        else:
            return None

    def find_user_id(self, email):
        asked_user = self._general_users_collection.find_one({"email": email})
        if asked_user:
            return asked_user['_id']
        else:
            return None

    def insert_fitness_user(self, fitness_user):
        user_id = self.find_user_id(fitness_user.email)
        fitness_user_json = fitness_user.encode()
        fitness_user_json["general_user_id"] = user_id
        self._fitness_users_collection.insert_one(fitness_user_json)

    def insert_service(self, service):
        self._service_collection.insert_one(service.encode())

    def get_service_id(self, service_name):
        asked_service = self._service_collection.find_one({'service_name' : service_name});
        if asked_service:
            return asked_service['_id']
        else:
            return None

    def insert_trainer(self, trainer):
        self._trainer_collection.insert_one(trainer.encode())
        pass




if __name__ == "__main__":
    dbe = DataBaseEntry()
    user = User("mail@m-heerde.de", "1234", "Matthias", "Heerde")
    dbe.insert_user(user)

    fitness_user = FitnessUser("mail@m-heerde.de", "05.08.1990", 90, 176)
    dbe.insert_fitness_user(fitness_user)


    print(dbe.find_user("mail@m-heerde.de"))