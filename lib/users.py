from vlib import db
from vlib.datatable import DataTable
from vlib.odict import odict
from vlib.utils import lazyproperty

DEBUG = 0

class UserError(Exception): pass

class User(DataTable):
    '''Preside over a single User'''

    def __init__(self, id):
        '''Create a User Object given a user_id
        '''
        self.db = db.getInstance()
        DataTable.__init__(self, self.db, 'users')
        self.id = id
        self.debug_sql = DEBUG
        self._loadData()

    def _loadData(self):
        '''Read a single User DB record'''
        self.setFilters('id=%s' % self.id)
        results = self.getTable()
        if not results:
            raise UserError('User not found. Id: %s' % self.id)
        self.__dict__.update(results[0])

    @lazyproperty
    def fullname(self):
        return '%s %s' % (self.first_name, self.last_name)
