from vlib import db
from vlib import conf
from vlib.datatable import DataTable
from vlib.utils import lazyproperty

from record import Record

from users import User
from jinja2.utils import urlize

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

    def getUserMessages(self, user_id, type=None):
        '''Return a all messages this users follows
           if type == 'my', then return this users messages.
           Data structure:
           messages: [ {id: x, text: y, ...},
                       {id: z, text: a, ...},
                       ... ]
        '''
        if type == 'my':
            sql_file = 'my_messages.sql'
        else:
            sql_file = 'user_messages.sql'

        sql_filepath = '%s/sql/templates/%s' % (self.conf.basedir, sql_file)
        sql = open(sql_filepath, 'r').read().replace('<user_id>', str(user_id))
        data = {
            'messages': [
                {'id'      : r['id'],
                 'user_id' : r['user_id'],
                 'author'  : r['author'],
                 'text'    : urlize(r['text'], target='_blank')
                 'created' : r['created'],
                 'reason'  : r['reason'],
                 }
                for r in self.db.query(sql)]
            }
        return data

    def getMyMessages(self, user_id):
        return self.getUserMessages(user_id, type='my')

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
