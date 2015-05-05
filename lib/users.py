from vlib import db
from vlib.utils import lazyproperty

from record import Record

DEBUG = 0

class UserError(Exception): pass

class User(Record):
    '''Preside over a single User'''

    def __init__(self, id):
        Record.__init__(self, db.getInstance(), 'users', id)

    @lazyproperty
    def fullname(self):
        return '%s %s' % (self.first_name, self.last_name)
