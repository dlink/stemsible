from vlib import db
from vlib.utils import lazyproperty

from record import Record

from users import User

class Messages(object):

    def get(self):
        o = []
        for m in reversed(range(1,8)):
            o.append(Message(m))
        return o

class Message(Record):
    '''Preside over a single Message'''

    def __init__(self, id):
        Record.__init__(self, db.getInstance(), 'messages', id)

    @lazyproperty
    def user(self):
        return User(self.user_id)
