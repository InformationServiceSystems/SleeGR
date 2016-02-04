import unittest
from database.models import User, Trainer


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
            '_type': 'general_user',
            'email': 'test@mail.de',
            'password': '1234',
            'first_name': 'Max',
            'last_name': 'Mustermann'

        }

        user = User.decode(user_json)

        self.assertEqual(user.email, 'test@mail.de',
                         'wrong email after initialization')
        self.assertEqual(user.first_name, 'Max',
                         'wrong firist name after initialization')
        self.assertEqual(user.last_name, 'Mustermann',
                         'wrong last name after initialization')
        self.assertEqual(user.password, '1234',
                         'wrong password after initialization')


class TestTrainer(unittest.TestCase):
    def test_trainer_encode(self):
        trainer = Trainer('56b311fb9b1467190d54hce', '56eedfffb9b1467190d54hce')
        trainer_json = trainer.encode()
        self.assertEqual(trainer_json['_type'], 'trainer', 'wrong type after encode')
        self.assertEqual(trainer_json['service_id'], trainer._service_id,
                         'wrong service_id after encode')
        self.assertEqual(trainer_json['general_user_id'], trainer._general_user_id,
                         'wrong general_user_id after encode')

    def test_trainer_decode(self):
        trainer_json = {
            '_type': 'trainer',
            'service_id': '1234abc',
            'general_user_id': 'abc123'
        }
        trainer = Trainer.decode(trainer_json)
        self.assertEqual(trainer._user_type, 2 , 'wrong user_type after decoding')
        self.assertEqual(trainer._general_user_id, trainer_json['general_user_id'],
                         'wrong general_user_id after decoding')
        self.assertEqual(trainer._service_id, trainer_json['service_id'],
                         'wrong servide_id after decoding')


class TestFitnessUser(unittest.TestCase):
    pass