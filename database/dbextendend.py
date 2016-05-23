from database.database import DbBase
import names

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
        return self.db_base._db['heart_rate'].find({'date' : date, 'user_id' : user})

    def find_sleep_data(self, date, user):
        pass
        #self.db_base._db['sleep_data'].insert_one(json)

    def find_fitness_data(self, measurement_type, date, user):
        pass
        #self.db_base._db[str(measurement_type)].insert_one(json)
