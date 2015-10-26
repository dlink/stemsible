#!/usr/bin/env python

from datetime import datetime
import unittest

from users import Users, User

# Fixtures

ID = 1
EMAIL = 'dvlink@gmail.com'
FIRST_NAME = 'David'
LAST_NAME = 'Link'
FULLNAME = 'David Link'
CREATED = '2015-07-24 17:40:53'

class TestUsers(unittest.TestCase):
    '''Test Users'''

    def test_getUser(self):
        user = User(ID)
        self.assertEqual(user.id, ID)
        self.assertEqual(user.first_name, FIRST_NAME)
        self.assertEqual(user.last_name, LAST_NAME)
        self.assertEqual(str(user.created), CREATED)
        self.assertTrue(isinstance(user.last_updated, datetime))

    def test_getUserFullname(self):
        user = User(ID)
        self.assertEqual(user.fullname, FULLNAME)

if __name__ == '__main__':
    unittest.main()
