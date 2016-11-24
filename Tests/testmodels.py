import unittest

import names
from databasemodels.models import User, Trainer, FitnessUser, Service


class TestUser(unittest.TestCase):
    def test_user(self):
        user = User('test@mail.de', '1234', 'Max', 'Mustermann')
        self.assertEqual(user.email, 'test@mail.de',
                         'wrong email after initialization')
        self.assertEqual(user.first_name, 'Max',
                         'wrong firist name after initialization')
        self.assertEqual(user.last_name, 'Mustermann',
                         'wrong last name after initialization')
        self.assertEqual(user.password, '1234',
                         'wrong password after initialization')

    def test_user_encode(self):
        user = User('test@mail.de', '1234', 'Max', 'Mustermann')
        user_json = user.encode()
        self.assertEqual(user_json['_type'], 'general_user',
                         'wrong type after encode')
        self.assertEqual(user_json['email'], 'test@mail.de',
                         'wrong email after encode')
        self.assertEqual(user_json['password'], '1234',
                         'wrong password after encode')
        self.assertEqual(user_json['first_name'], 'Max',
                         'wrong first name after encode')
        self.assertEqual(user_json['last_name'], 'Mustermann',
                         'wrong  last name after encode')

    def test_user_decode(self):
        user_json = {
            names.type: names.user_type_names.user_general,
            names.email: 'test@mail.de',
            names.password: '1234',
            names.first_name: 'Max',
            names.last_name: 'Mustermann'

        }

        user = User.decode(user_json)


        self.assertEqual('Max', user.first_name,
                         'wrong firist name after initialization')
        self.assertEqual('Mustermann', user.last_name,
                         'wrong last name after initialization')
        self.assertEqual('1234', user.password,
                         'wrong password after initialization')


class TestTrainer(unittest.TestCase):
    def test_trainer_encode(self):
        trainer = Trainer('56b311fb9b1467190d54hce',
                          '56eedfffb9b1467190d54hce')
        trainer_json = trainer.encode()
        self.assertEqual(names.user_type_names.user_trainer, trainer_json['_type'],
                         'wrong type after encode')
        self.assertEqual(trainer_json['service_id'], trainer._service_id,
                         'wrong service_id after encode')
        self.assertEqual(trainer_json['general_user_id'],
                         trainer._general_user_id,
                         'wrong general_user_id after encode')

    def test_trainer_decode(self):
        trainer_json = {
            '_type': names.user_type_names.user_trainer,
            'service_id': '1234abc',
            'general_user_id': 'abc123'
        }
        trainer = Trainer.decode(trainer_json)
        self.assertEqual(trainer._user_type, 2,
                         'wrong user_type after decoding')
        self.assertEqual(trainer._general_user_id,
                         trainer_json['general_user_id'],
                         'wrong general_user_id after decoding')
        self.assertEqual(trainer._service_id, trainer_json['service_id'],
                         'wrong servide_id after decoding')


class TestFitnessUser(unittest.TestCase):
    def test_fitness_user_encode(self):
        user = FitnessUser('123abc', '05.08.1990', 75, 178)
        user_json = user.encode()
        self.assertEqual(user_json['_type'], 'fitness_user',
                         'wrong _type after encoding')
        self.assertEqual(user_json['user_type'], user._user_type,
                         'wrong user_type after encoding')
        self.assertEqual(user_json[names.birthday], user._birthday,
                         'wrogn birthday after encoding')
        self.assertEqual(user_json['weight'], user._weight,
                         'wrogn weight after encoding')
        self.assertEqual(user_json['height'], user._height,
                         'wrogn height after encoding')
        self.assertEqual(user_json['general_user_id'], user._general_user_id,
                         'wrogn general_user_id after encoding')

    def test_fitness_user_decode(self):
        user_json = {
            '_type': 'fitness_user',
            'user_type': 1,
            'birthday': '05.08.1990',
            'weight': 75,
            'height': 178,
            'general_user_id': '123abc'
        }
        user = FitnessUser.decode(user_json)
        self.assertEqual(user._birthday, user_json[names.birthday],
                         'wrong birthday after decoding')
        self.assertEqual(user._height, user_json['height'],
                         'wrong height after decoding')
        self.assertEqual(user._general_user_id, user_json['general_user_id'],
                         'wrong general_user_id after decoding')
        self.assertEqual(user._user_type, user_json['user_type'],
                         'wrong user_type after decoding')
        self.assertEqual(user._weight, user_json['weight'],
                         'wrong weight after decoding')


class TestGeneralService(unittest.TestCase):
    def test_service_encode(self):
        service = Service('test_service', 5)
        service_json = service.encode()
        self.assertEqual('general_service', service_json['_type'],
                         'wrong _type after encoding')
        self.assertEqual(service_json['service_name'], service._service_name,
                         'wrong service_name after encoding')
        self.assertEqual(service_json['allowed_users'], service._allowed_users,
                         'wrong allowed_users number after encoding')

    def test_service_decode(self):
        pass
