from datetime import datetime

from vlib import db
from vlib.datatable import DataTable

class UserSchools(DataTable):

    def __init__(self):
        DataTable.__init__(self, db.getInstance(), 'user_schools')

    def add(self, data):
        data['created'] = datetime.now()
        id = self.insertRow(data)
        return id # UserSchool(id).data
