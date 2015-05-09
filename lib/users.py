from vlib import db
from vlib.datatable import DataTable
from vlib.utils import lazyproperty

from record import Record

DEBUG = 0

class UserError(Exception): pass

class Users(DataTable):
    def __init__(self):
        DataTable.__init__(self, db.getInstance(), 'users')

class User(Record):
    '''Preside over a single User'''

    def __init__(self, id):
        Record.__init__(self, db.getInstance(), 'users', id)
        self.data['fullname'] = '%s %s' % (self.first_name, self.last_name)
