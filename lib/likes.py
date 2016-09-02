from vlib import db
from record import Record

class Like(Record):
    '''Preside over a single Like'''

    def __init__(self, id):
        Record.__init__(self, db.getInstance(), 'likes', id)
