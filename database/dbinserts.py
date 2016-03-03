import names
from database.database import DbBase
from databasemodels.models import User


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
        self.db_base._user_map_collection.insert_one(service.encode)

    def find_user(self, email):
        asked_user_json = self.db_base._general_users_collection.find_one({names.email: email})
        if asked_user_json:
            return User.decode(asked_user_json)
        else:
            return None


'''

if __name__ == "__main__":
    dbe = DataBaseEntry()
    user = User("mail@m-heerde.de", "1234", "Matthias", "Heerde")
    dbe.insert_user(user)
    fitness_user = FitnessUser("mail@m-heerde.de", "05.08.1990", 90, 176)
    dbe.insert_fitness_user(fitness_user)
    print ((dbe.get_user_id("mail@m-heerde.de")))
    print(dbe.find_user("mail@m-heerde.de"))
    dbe._fitness_users_collection.drop()
    '''