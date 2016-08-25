#!/usr/bin/env python

from datetime import datetime

from vlib import db
from vlib.datatable import DataTable
from vlib import conf
from vlib.utils import format_datetime
from record import Record

UNKNOWN_ADDRESS_ID = 0
UNKNOWN_DISTRICT_ID = 0

class SchoolError(Exception): pass

class Schools(DataTable):

    def __init__(self):
        DataTable.__init__(self, db.getInstance(), 'schools')
        self.conf = conf.getInstance()

    def getSchools(self, filters):
        '''Given a filter
           Return a list of Instantiated School Objects

           filter is anything accepted by DataTable.setFilters()
           ex. school = Schools().getSchools({'name': 'My School'})[0]
        '''
        self.setFilters(filters)
        self.setColumns('id')
        o = []
        for row in self.getTable():
            o.append(School(row['id']))
        return o

    def add(self, data):
        data['created'] = datetime.now()
        id = self.insertRow(data)
        return School(id).data

    def genJson(self):
        '''Generate the schools Json Data used by registration
           typeahead buffer
        '''
        datafile = '%s/web/data/schools.json' % self.conf.basedir

        sql = 'select name from schools order by name'
        names = [s['name'] for s in self.db.query(sql)]
        names_str = ",".join(['"%s"' % n for n in names])
        json = '[' + names_str + ']\n'
        open(datafile, 'w').write(json.encode('utf-8'))
        return '%s schools updated' % len(names)

    def missingAddresses(self):
        '''Return a csv formated table as a STR of
           All schools with unknown address_id
        '''
        file = '%s/lib/sql/missing_school_addresses.sql' % self.conf.basedir
        sql = open(file, 'r').read()
        o = ''
        for row in self.db.query(sql):
            row['created'] = format_datetime(row['created'])
            o += '{num_users}, {school_id}, {name}, {created}\n'.format(**row)
        return o

class School(Record):
    '''Preside over a single School'''

    def __init__(self, id):
        Record.__init__(self, db.getInstance(), 'schools', id)
        self._loadAdditionalData()

    def _loadAdditionalData(self):
        pass

if __name__ == '__main__':
    import sys

    CMD = 'gen_json'
    if len(sys.argv) < 2 or sys.argv[1] != CMD:
        print 'schools.py %s' % CMD
        sys.exit(1)

    print Schools().genJson()
