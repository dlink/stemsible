from vlib.datatable import DataTable
from vlib.odict import odict

DEBUG = 0

class RecordError(Exception): pass

class Record(DataTable):
    '''Preside over a single Db Record'''

    def __init__(self, db, table, id):
        '''Create a Record Object given
              a vlib.db Object, a table name, and a record Id
        '''
        self.db    = db      
        self.table = table
        self.id    = id

        DataTable.__init__(self, db, table)
        self.debug_sql = DEBUG
        self._loadData()

    def _loadData(self):
        '''Read a single Dbrecord DB record'''
        self.setFilters('id=%s' % self.id)
        results = self.getTable()
        if not results:
            raise DbrecordError('Dbrecord not found. Id: %s' % self.id)
        self.__dict__.update(results[0])

