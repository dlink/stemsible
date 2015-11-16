#!/usr/bin/env python

#from datetime import datetime
import unittest

from vlib import db

from registration import Registration

# Fixtures
SCHOOLID   = 2
SCHOOLNAME = 'Legacy Elementary'
SCHOOLNAME_NOTFOUND = '__Unit Test School__'

class TestRegistrations(unittest.TestCase):
    '''Test Registrations'''

    def setUp(self):
        self.db = db.getInstance()

    def test_getSchoolId(self):
        school_id = Registration()._getSchoolId(SCHOOLNAME)
        self.assertEqual(school_id, SCHOOLID)

    def test_getSchoolId_CreateNew(self):
        max_school_id = self._getMaxSchoolId()
        school_id = Registration()._getSchoolId(SCHOOLNAME_NOTFOUND)
        self.assertEqual(school_id, max_school_id+1)
        self._removeNewSchool(school_id)

    def _getMaxSchoolId(self):
        sql = 'select max(id) as max_id from schools'
        return self.db.query(sql)[0]['max_id']

    def _removeNewSchool(self, school_id):
        '''Remove the new Unit Test School Record
           and set the Auto_increment back
        '''
        sql = 'delete from schools where id = %s'
        self.db.execute(sql, params=[school_id])

        # reset auto_increment
        alter_sql = 'alter table schools auto_increment = 1'
        self.db.execute(alter_sql)

if __name__ == '__main__':
    unittest.main()
