import decorators
import names


class User:

    @decorators.check_user
    def __init__(self, email, password, first_name=None, last_name=None):
        self._email = email
        self._password = password
        self._fist_name = first_name
        self._last_name = last_name

    @property
    def email(self):
        return self._email

    @property
    def password(self):
        return self._password

    @property
    def first_name(self):
        return self._fist_name

    @property
    def last_name(self):
        return self._last_name

    def encode(self):
        return {
            names.type: names.user_type_names.user_general,
            names.email: self._email,
            names.password: self._password,
            names.first_name: self._fist_name,
            names.last_name: self._last_name
        }

    @classmethod
    def decode(cls, user_json):
        assert user_json[names.type] == names.user_type_names.user_general
        if names.first_name not in user_json:
            user_json[names.first_name]= None
        if names.last_name not in user_json:
            user_json[names.last_name] = None
        return User(user_json[names.email], user_json[names.password], user_json[names.first_name],
                    user_json[names.last_name])

    def __str__(self):
        return '%s' % (self._email)


class FitnessUser:
    def __init__(self, general_user_id, birthday, weight, height):
        self._general_user_id = general_user_id
        self._user_type = 1
        self._birthday = birthday
        self._weight = weight
        self._height = height

    @property
    def general_user_id(self):
        return self._general_user_id

    @property
    def birth_day(self):
        return self._birthday

    @property
    def weight(self):
        return self._weight

    @property
    def height(self):
        return self._height

    def encode(self):
        return {
            names.type: names.user_type_names.user_fitness,
            names.user_type: self._user_type,
            names.birthday: self._birthday,
            names.weight: self._weight,
            names.height: self._height,
            names.general_user_id: self._general_user_id
        }

    @classmethod
    def decode(cls, fitness_user):
        assert fitness_user[names.type] == names.user_type_names.user_fitness
        return FitnessUser(fitness_user[names.general_user_id], fitness_user[names.birthday],
                           fitness_user[names.weight],
                           fitness_user[names.height])


class Service:
    def __init__(self, service_name, allowed_users):
        self._service_name = service_name
        self._allowed_users = allowed_users

    def encode(self):
        return {
            names.type: names.service_type_names.service_general,
            names.service_name: self._service_name,
            names.service_allowed_users: self._allowed_users
        }

    @classmethod
    def decode(cls, service):
        assert service[names.type] == names.service_type_names.service_general
        return User(service[names.service_name], service[names.service_allowed_users])


class Trainer:
    def __init__(self, service_id, general_user_id):
        self._general_user_id = general_user_id
        self._service_id = service_id
        self._user_type = 2

    def encode(self):
        return {
            names.type: names.user_type_names.user_trainer,
            names.general_user_id: self._general_user_id,
            names.service_id: self._service_id,
            names.user_type: self._user_type
        }

    @classmethod
    def decode(cls, trainer):
        assert trainer[names.type] == names.user_type_names.user_trainer
        return Trainer(trainer[names.service_id],
                       trainer[names.general_user_id])


class ServiceUserMap:
    def __init__(self, service_id, user_id):
        self._general_service_id = service_id
        self._general_user_id = user_id

    @property
    def genera_user_id(self):
        return self._general_user_id

    @property
    def general_service_id(self):
        return self._general_service_id

    def encode(self):
        return {
            names.type: names.service_type_names.service_user_map,
            names.service_id: self._general_service_id,
            names.user_id: self._general_user_id
        }

    @classmethod
    def decode(cls, service_json):
        if service_json[names.type] == names.service_type_names.service_user_map:
            return ServiceUserMap(service_json[names.service_id],
                                  service_json[names.user_id])
