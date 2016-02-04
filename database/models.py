class User:
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
            '_type': 'general_user',
            'email': self._email,
            'password': self._password,
            'first_name': self._fist_name,
            'last_name': self._last_name
        }

    @classmethod
    def decode(cls, user):
        assert user['_type'] == 'general_user'
        return User(user['email'], user['password'], user['first_name'],
                    user['last_name'])

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
            '_type': 'fitness_user',
            'user_type': self._user_type,
            'birthday': self._birthday,
            'weight': self._weight,
            'height': self._height,
            'general_user_id': self._general_user_id
        }

    @classmethod
    def decode(cls, fitness_user):
        assert fitness_user['_type'] == 'general_user'
        return User(fitness_user['general_user_id'], fitness_user['birthday'],
                    fitness_user['weight'],
                    fitness_user['height'])


class Service:
    def __init__(self, service_name, allowed_users):
        self._service_name = service_name
        self._allowed_users = allowed_users

    def encode(self):
        return {
            '_type': 'service',
            'service_name': self._service_name,
            'allowed_users': self._allowed_users
        }

    @classmethod
    def decode(cls, service):
        assert service['_type'] == 'general_user'
        return User(service['service_name'], service['allowed_users'])


class Trainer:
    def __init__(self, service_id, general_user_id):
        self._general_user_id = general_user_id
        self._service_id = service_id
        self._user_type = 2

    def encode(self):
        return {
            '_type': 'trainer',
            'general_user_id': self._general_user_id,
            'service_id': self._service_id,
            'user-type': self._user_type
        }

    @classmethod
    def decode(cls, trainer):
        assert trainer['_type'] == 'trainer'
        return Trainer(trainer['service_id'],
                    trainer['general_user_id'])


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
            '_type': 'ServiceUserMap',
            'general_service_id': self._general_service_id,
            'general_user_id': self._general_user_id
        }

    @classmethod
    def decode(cls, service_json):
        if service_json['_type'] == 'ServiceUserMap':
            return ServiceUserMap(service_json['general_service_id'],
                                  service_json['general_user_id'])
