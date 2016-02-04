import unittest

from database.databaseentry import DataBaseEntry

class TestDataBaseEntry(unittest.TestCase):
    def __init__(self):
        self._dbe = DataBaseEntry()
