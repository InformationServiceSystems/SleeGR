from pymongo import MongoClient

class DbBase:
    def __init__(self, db_name='triathlon'):
        _server_name = 'localhost'
        _mongodb_port = 27017
        self._client = MongoClient(_server_name, _mongodb_port)
        self._db = self._client[db_name]
        self._pathmate_db = self._client['PM2']
        self._general_users_collection = self._db.general_user
        self._fitness_users_collection = self._db.fitness_user
        self._service_collection = self._db.general_service
        self._trainer_collection = self._db.trainer_user
        self._user_map_collection = self._db.user_map_service

