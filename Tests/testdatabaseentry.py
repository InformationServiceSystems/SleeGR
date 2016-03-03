import unittest

from Tests.setuptestdatabase import testDataBase


class TestDataBaseEntry(unittest.TestCase):
    def setUp(self):
        self.test = testDataBase();

    def test_find_user_no_names(self):
        new_user = self.test.entry.find_user(self.test.user._email)
        self.assertEqual(new_user._email, self.test.user._email, 'wrong email')
        self.assertEqual(new_user._password, self.test.user._password, 'wrong password')
        self.assertIsNone(new_user._fist_name, 'first_name should be None')
        self.assertIsNone(new_user._last_name, 'last_name should be None')

    def test_find_user_with_names(self):
        new_user = self.test.entry.find_user(self.test.user1._email)
        self.assertEqual(new_user._email, self.test.user1._email, 'wrong email')
        self.assertEqual(new_user._password, self.test.user1._password, 'wrong password')
        self.assertEqual(new_user._fist_name, 'Max', 'first_name is wrong')
        self.assertEqual(new_user._last_name, self.test.user1._last_name, 'last_name should is wrong')

    def test_add_fitness_user(self):
        pass

