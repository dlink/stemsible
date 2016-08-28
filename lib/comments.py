from vlib import db
from record import Record

class Comment(Record):
    '''Preside over a single Comment'''

    def __init__(self, id):
        Record.__init__(self, db.getInstance(), 'messages', id)
