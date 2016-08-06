
from datetime import datetime

from vlib import db
from vlib.datatable import DataTable
from vlib import conf
from record import Record

UNKNOWN_ADDRESS_ID = 1
UNKNOWN_DISTRICT_ID = 1

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

    def genTypeAheadData(self):
        '''Generate the schools Json Data used by registration
           typeahead buffer
        '''
        datafile = '%s/web/data/schools.json' % self.conf.basedir

        sql = 'select name from schools order by name'
        data = [str(s['name']) for s in self.db.query(sql)]
        open(datafile, 'w').write(str(data) + '\n')
        return '%s schools updated' % len(data)

class School(Record):
    '''Preside over a single School'''

    def __init__(self, id):
        Record.__init__(self, db.getInstance(), 'schools', id)
        self._loadAdditionalData()

    def _loadAdditionalData(self):
        pass

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2 or sys.argv[1] != 'gen_typeahead_data':
        print 'schools.py gen_typeahead_data'
        sys.exit(1)

    print Schools().genTypeAheadData()
