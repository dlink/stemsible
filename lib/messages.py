
import re

from vlib import db
from vlib import conf
from vlib import logger
from vlib.datatable import DataTable
from vlib.utils import lazyproperty

from record import Record

from users import User
from comments import Comment
from likes import Like
from activitynotifications import ActivityNotifications

class Messages(DataTable):

    @lazyproperty
    def logger(self):
        return logger.getLogger('Messages')

    def __init__(self):
        self.db = db.getInstance()
        self.conf = conf.getInstance()
        self.activity_notifications = ActivityNotifications()
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
            message.addUrlPreviews()

            results = message.data
            results['user'] = message.user.data

            text = message.data['text']
            text = text if len(text) < 40 else text[0:40] + ' ...'

            self.logger.info('%s: new message: %s, %s'
                             % (results['user']['email'], id, text))

            # record comments for later notification
            if results.get('reference_id'):
                self.activity_notifications.registerComment(results)

            return results

        except Exception, e:
            self.logger.error("new message failed: %s: %s" % (data, e))
            return {'error': str(e), 'data': str(data)}

    def checkForDups(self):
        '''-- Problem statement

        -- After user creates a new comment, or creates a new post --
           if they immediately refresh the page (with Ctrl-R for
           example), the previous HTML POST data is repeated. And
           their data update is repeated. You can verify this is dev
           or staging.
        
        -- This pattern seems to be the solution;
        -- https://en.wikipedia.org/wiki/Post/Redirect/Get
        
        -- In the mean time we can remove duplicate entries from the database
        
        
        -- This query lists dupicate messages (or comments).
        '''

        sql = '''
        select
           u.id as user_id,
           concat_ws(' ', u.first_name, u.last_name) as user_fullname,
           m.created,
           m.text,
           m.reference_id
        from
           messages m
           join (
              select
                 text,
                 count(*)
              from
                 messages
              group by
                 1
              having
                 count(*) > 1
           ) m2 on m.text = m2.text
           join users u on m.user_id = u.id
        order by
           m.text,
           m.id
        '''

        from vlib.utils import format_datetime
        
        old_text = None
        dups = []
        report = ''
        
        for row in self.db.query(sql):
            user_id       = str(row['user_id'])
            user_fullname = row['user_fullname']
            created       = format_datetime(row['created'])
            text          = row['text'][0:50]
            reference_id  = str(row['reference_id'])
            
            print_rec = ', '.join(
                [user_id, user_fullname, created, text, reference_id])

            # rec text same as last one?
            if old_text and text != old_text:
                report += '\n'.join(dups) + '\n\n'
                dups = []

            dups.append(print_rec)
            old_text = text
        
        if dups:
            report += '\n'.join(dups) + '\n\n'
            dups = []

        if report:
            from emails import Emails
            Emails().send_email(
                'dvlink@gmail.com,udaydotkumar@gmail.com',
                'Dupliate Messages Report',report)
            
class Message(Record):
    '''Preside over a single Message'''

    def __init__(self, id):
        self.db = db.getInstance()
        self.conf = conf.getInstance()
        Record.__init__(self, self.db, 'messages', id)

    @lazyproperty
    def comments(self):
        comments = []
        sql = 'select id from messages where reference_id = %s'
        for row in self.db.query(sql, params=[self.id]):
            comments.append(Comment(row['id']))
        return comments
    @lazyproperty
    def likes(self):
        likes = []
        sql = 'select id from likes where message_id = %s'
        for row in self.db.query(sql, params=[self.id]):
            likes.append(Like(row['id']))
        return likes
    
    @lazyproperty
    def url_previews(self):
        '''Get url preview data'''
        self.url_previewsDt.setFilters({'message_id': self.id})
        return self.url_previewsDt.getTable()

    @lazyproperty
    def user(self):
        return User(self.user_id)

    @lazyproperty
    def urls(self):
        from urls import Urls
        return Urls()

    @lazyproperty
    def urlPreview(self):
        from url_preview import UrlPreview
        return UrlPreview()

    @lazyproperty
    def url_previewsDt(self):
        from vlib.datatable import DataTable
        return DataTable(self.db, 'url_previews')

    def addUrlPreviews(self):
        '''Extract urls from message text
           Call UrlPreview
           Write url preview data fields to database
        '''
        for url in self.urls.extractUrls(self.text):
            preview = self.urlPreview.getData(url)
            if preview.get('error'):
                continue

            # no pdf support, which returns an html field, but no 'url'
            if not preview.get('url'):
                return ''

            data = {'message_id': self.id}
            for f in self.urlPreview.FIELDS:
                data[f] = preview.get(f)
            self.url_previewsDt.replaceRow(data)

def gen_all_url_previews():
    for m in range(1,420):
        print m
        try:
            message = Message(m)
        except:
            print 'skipping', m
            continue
        message.addUrlPreviews()

if __name__ == '__main__':
    from vlib.utils import pretty
    
    id = 431
    #cmd = 'get_data'
    #cmd = 'get_url_preview_data'
    cmd = 'gen_all'
    
    if cmd == 'get_data':
        m = Message(id)
        print pretty(m.data)
    elif cmd == 'get_url_preview_data':
        m = Message(id)
        for preview in m.url_previews:
            print pretty(preview)
            print
    elif cmd == 'gen_all':
        gen_all_url_previews()
    else:
        print 'cmd unknown:', cmd
