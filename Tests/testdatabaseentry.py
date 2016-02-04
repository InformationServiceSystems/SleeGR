import unittest

from database.databaseentry import DataBaseEntry
from database.models import User


class TestDataBaseEntry(unittest.TestCase):
    def setUp(self):
        self._entry = DataBaseEntry()
        self._entry._general_users_collection.drop()

    def test_find_user_no_names(self):
        user = User('testl@mail.de', '1234')
        self._entry.insert_user(user)
        new_user = self._entry.find_user(user._email)
        self.assertEqual(new_user._email, user._email, 'wrong email')
        self.assertEqual(new_user._password, user._password, 'wrong password')
        self.assertIsNone(new_user._fist_name, 'first_name should be None')
        self.assertIsNone(new_user._last_name, 'last_name should be None')

    def test_find_user_with_names(self):
        user = User('testl@mail.de', '1234', 'Max', 'Mustermann')
        self._entry.insert_user(user)
        new_user = self._entry.find_user(user._email)
        self.assertEqual(new_user._email, user._email, 'wrong email')
        self.assertEqual(new_user._password, user._password, 'wrong password')
        self.assertEqual(new_user._fist_name, 'Max', 'first_name is wrong')
        self.assertEqual(new_user._last_name, user._last_name, 'last_name should is wrong')

    def test_add_fitness_user(self):
        pass

