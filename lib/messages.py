from vlib import db
from vlib import conf
from vlib.datatable import DataTable
from vlib.utils import lazyproperty

from record import Record

from users import User

class Messages(DataTable):

    def __init__(self):
        self.db = db.getInstance()
        self.conf = conf.getInstance()
        DataTable.__init__(self, db.getInstance(), 'messages')

    def getMessages(self):
        sql_file = '%s/sql/templates/messages.sql' % self.conf.basedir
        sql = open(sql_file, 'r').read()
        data = {
            'messages': [
                {'id'      : r['id'],
                 'user_id' : r['user_id'],
                 'author'  : r['author'],
                 'text'    : r['text'],
                 'created' : r['created'],
                 }
                for r in self.db.query(sql)]
            }
        return data

    def getUserMessages(self, user_id):
        sql_file = '%s/sql/templates/user_messages.sql' % self.conf.basedir
        sql = open(sql_file, 'r').read().replace('<user_id>', str(user_id))
        data = {
            'messages': [
                {'id'      : r['id'],
                 'user_id' : r['user_id'],
                 'author'  : r['author'],
                 'text'    : r['text'],
                 'created' : r['created'],
                 'reason'  : r['reason'],
                 }
                for r in self.db.query(sql)]
            }
        return data

    def add(self, data):
        try:
            id = self.insertRow(data)
            message = Message(id)
            results = message.data
            results['user'] = message.user.data
            return results
        except Exception, e:
            return {'error': str(e),
                    'data': str(data)}

class Message(Record):
    '''Preside over a single Message'''

    def __init__(self, id):
        Record.__init__(self, db.getInstance(), 'messages', id)

    @lazyproperty
    def user(self):
        return User(self.user_id)
