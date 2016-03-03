import unittest
from threading import Thread
import requests
import time
'''
from Tests.setuptestdatabase import testDataBase
#class runApp():
#    def __init__(self):
#        from webpage import app
#        self.app = app



class TestViwes(unittest.TestCase):
    def setUp(self):
        #t = Thread(target=runApp())
        #t.start()
        self.test = testDataBase()

    def testUser(self):
        data = self.test.user.encode()
        re = requests.post('http://127.0.0.1:5000/login_rest',json=data)
        print(re.text)
        assert(True)'''