
from vlib import db
from vlib.attributes import Attributes

class SchoolRelationships(Attributes):
    '''Preside over School Relationships'''

    def __init__(self):
        db_ = db.getInstance()
        Attributes.__init__(self, db_, 'school_relationships', 'id')
