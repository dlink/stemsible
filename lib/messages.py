
import re

from vlib import db
from vlib import conf
from vlib import logger
from vlib.datatable import DataTable
from vlib.utils import lazyproperty

from record import Record

from users import User

class Messages(DataTable):

    @lazyproperty
    def logger(self):
        return logger.getLogger('Messages')

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

    def getUserMessages(self, user_id=None, type=None, search=None):
        '''Return a all messages this users follows
           if search passed in then return search result messages.
           if type == 'my', then return this users messages.
           otherwise return user feed messages
           Data structure:
           messages: [ {id: x, text: y, ...},
                       {id: z, text: a, ...},
                       ... ]
        '''
        if search:
            sql_file = 'search_messages.sql'
        elif type == 'my':
            sql_file = 'my_messages.sql'
        else:
            sql_file = 'user_messages.sql'

        sql_filepath = '%s/sql/templates/%s' % (self.conf.basedir, sql_file)

        if search:
            sql = open(sql_filepath, 'r').read().replace('<search>', search)
        else:
            sql = open(sql_filepath, 'r').read().replace('<user_id>',
                                                         str(user_id))
        def adj_reason(reason):
            '''Given reason as semicolon sep. list like this:
               'Parent - Ashburn, VA ; Interest - Ashburn, VA'
               Remove any 'Interest' fields unless it is the only one
            '''
            if 'Interest' in reason:
                parts = []
                for p in reason.split(' ; '):
                    if 'Interest' not in  p:
                        parts.append(p)
                if parts:
                    return ' ; '.join(parts)
                return reason
            return reason

        data = {
            'messages': [
                {'id'      : r['id'],
                 'user_id' : r['user_id'],
                 'author'  : r['author'],
                 'text'    : r['text'],
                 'created' : r['created'],
                 'reason'  : adj_reason(r['reason']),
                 }
                for r in self.db.query(sql)]
            }
        return data

    def getMyMessages(self, user_id):
        return self.getUserMessages(user_id, type='my')

    def getSearchMessages(self, search):
        # deal with apostrophes (')
        search = search.replace("'", "\\'")

        # searchq will be like: '+mic* +jagger*'
        search = re.sub('[+\-><\(\)~*\"@]', ' ', search)
        searchq = ' '.join(['+%s*' % n for n in search.strip().split(' ')])

        return self.getUserMessages(search=searchq)

    def add(self, data):
        try:
            id = self.insertRow(data)
            message = Message(id)
            results = message.data
            results['user'] = message.user.data

            text = message.data['text']
            text = text if len(text) < 40 else text[0:40] + ' ...'
            self.logger.info('%s: new message: %s, %s'
                             % (results['user']['email'], id, text))
            return results

        except Exception, e:
            self.logger.error("new message failed: %s: %s" % (data, e))
            return {'error': str(e),
                    'data': str(data)}

class Message(Record):
    '''Preside over a single Message'''

    def __init__(self, id):
        Record.__init__(self, db.getInstance(), 'messages', id)

    @lazyproperty
    def user(self):
        return User(self.user_id)
