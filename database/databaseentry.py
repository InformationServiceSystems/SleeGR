from pymongo import MongoClient

from database.models import User


class DataBaseEntry:

    def __init__(self):
        _server_name = 'localhost'
        _mongodb_port = 27017
        self.__client = MongoClient(_server_name, _mongodb_port)
        self.__db = self.__client.triathlon
        self.__general_users_collection = self.__db.user

    def insert_user(self, user):
        """
        Insert a user in the user collection.
        :param user: Need to be instance of User (see models.py)
        """
        self.__general_users_collection.insert_one(user.encode())

    def find_user(self, email):
        asked_user = self.__general_users_collection.find_one({"email" : email})
        if asked_user:
            return user.decode(asked_user)
        else:
            return None


if __name__ == "__main__":
    dbe = DataBaseEntry()
    user = User("1234", "mail@m-heerde.de", "1234", "Matthias", "Heerde")
    dbe.insert_user(user)
    print(dbe.find_user("mail@m-heerde.de"))