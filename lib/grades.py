
from vlib import db
from vlib.attributes import Attributes

class Grades(Attributes):
    '''Preside over Grades as an attribute of a User-School Relationship'''

    def __init__(self):
        db_ = db.getInstance()
        Attributes.__init__(self, db_, 'grades', 'id')
