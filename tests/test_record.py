#!/usr/bin/env python

from datetime import datetime
import unittest

from vlib import db

from record import Record, RecordError

# Fixtures

ID = 1
EMAIL = 'dvlink@gmail.com'
FIRST_NAME = 'David'
LAST_NAME = 'Link'
#CREATED = '2015-05-04 20:54:00'

class TestRecords(unittest.TestCase):
    '''Test Records using users table'''

    def test_getRecord(self):
        user = Record(db.getInstance(), 'users', ID)
        self.assertEqual(user.id, ID)
        self.assertEqual(user.first_name, FIRST_NAME)
        self.assertEqual(user.last_name, LAST_NAME)
        #self.assertEqual(str(user.created), CREATED)
        self.assertTrue(isinstance(user.last_updated, datetime))

    def test_getRecordFail(self):
        with self.assertRaises(RecordError):
            no_user = Record(db.getInstance(), 'users', 0)
            
if __name__ == '__main__':
    unittest.main()
