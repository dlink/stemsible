
from datetime import datetime

from vlib import db
from vlib.datatable import DataTable

class Follows(DataTable):
    '''Preside over what users follows which users'''

    def __init__(self):
        self.db = db.getInstance()
        DataTable.__init__(self, self.db, 'follows')

    def getFollows(self, user_id, follows_id):
        self.setFilters({'user_id': user_id, 'follows_id': follows_id})
        self.setColumns('*')
        o = []
        for row in self.getTable():
            o.append(row) # Follow(row['id']))
        return o

    def update(self, user):
        '''Given a user object
           Update all their follow connections

           Current Stub Algorithm:
              All users follow All users
        '''

        # TODO: Beef up this algorithm
        
        # get list of all other user Ids
        sql = 'select id from users'
        other_user_ids = [r['id'] for r in self.db.query(sql)]

        # user follows others
        for other_user_id in other_user_ids:
            follows_rec = {'user_id': user.id,
                           'follows_id': other_user_id,
                           'choice': 1,
                           'active': 1}
            if not self.getFollows(user.id, other_user_id):
                self.add(follows_rec)

        # other follows user
        for other_user_id in other_user_ids:
            follows_rec = {'user_id': other_user_id,
                           'follows_id': user.id,
                           'choice': 1,
                           'active': 1}
            if not self.getFollows(other_user_id, user.id):
                self.add(follows_rec)

    def add(self, data):
        data['created'] = datetime.now()
        id = self.insertRow(data)
        return id # Follow(id).data


if __name__ == '__main__':
    from users import User
    Follows().update(User(1))
