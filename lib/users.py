
from datetime import datetime

from vlib import db
from vlib.datatable import DataTable
from vlib.utils import lazyproperty

from record import Record

DEBUG = 0

class UserError(Exception): pass

class Users(DataTable):

    def __init__(self):
        DataTable.__init__(self, db.getInstance(), 'users')

    def getUsers(self, filters):
        '''Given a filter
           Return a list of Instantiated User Objects

           filter is anything accepted by DataTable.setFilters()
           ex. user = Users().getUsers({'email': 'dlink@gmail.com'})[0]
        '''
        self.setFilters(filters)
        self.setColumns('id')
        o = []
        for row in self.getTable():
            o.append(User(row['id']))
        return o

    def add(self, data):
        data['created'] = datetime.now()
        id = self.insertRow(data)
        return User(id)

class User(Record):
    '''Preside over a single User'''

    def __init__(self, id):
        Record.__init__(self, db.getInstance(), 'users', id)
        self._loadAdditionalData()

    def _loadAdditionalData(self):
        '''Add fullnames to self and to self.data
        '''
        fullname = '%s %s' % (self.first_name, self.last_name)
        self.data['fullname'] = fullname
        self.__dict__.update({'fullname': fullname})

    @lazyproperty
    def following(self):
        '''Return a list of User Objects of those this user follows'''
        dt = DataTable(self.db, 'follows')
        dt.setColumns(['follows_id'])
        dt.setFilters('user_id = %s' % self.id)
        o = []
        for record in dt.getTable():
            follows_id = record['follows_id']
            if follows_id == self.id:
                continue
            o.append(User(follows_id))
        return o
