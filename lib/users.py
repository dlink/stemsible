
from vlib.odict import odict

# Here are some fixed users:

USER_DATA = [{'id': 10, 'fullname': 'David Link'},
             {'id': 13, 'fullname': 'Jenny Doe'},
             {'id': 56, 'fullname': 'Jill Garner'},
             {'id': 108, 'fullname': 'Uday Kumar'}]

class UserError(Exception): pass

class User(object):

    def __init__(self, user_id):
        self.id = None

        for u in map(odict, USER_DATA):
            if u.id == user_id:
                self.id = u.id
                self.fullname = u.fullname
                break
        if not self.id:
            raise UserError('User not found. id: %s' % user_id)
                
            
