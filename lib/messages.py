from datetime import datetime

from vlib import db
from vlib.datatable import DataTable
from vlib.utils import lazyproperty

from record import Record

from users import User

class Messages(DataTable):

    def __init__(self):
        DataTable.__init__(self, db.getInstance(), 'messages')

    def get(self):
        o = []
        for m in reversed(range(1,8)):
            o.append(Message(m))
        return o

    def add(self, data):
        try:
            data['created'] = datetime.now()
            id = self.insertRow(data)
            message = Message(id)
            results = message.data
            results['user'] = message.user.data
            return results
        except Exception, e:
            return {'error': str(e)}

class Message(Record):
    '''Preside over a single Message'''

    def __init__(self, id):
        Record.__init__(self, db.getInstance(), 'messages', id)

    @lazyproperty
    def user(self):
        return User(self.user_id)
