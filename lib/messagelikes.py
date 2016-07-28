from vlib import conf
from vlib import db
from vweb.html import *


js_files = ['js/likes.js']
css_files = ['css/likes.css']

def addHeaders(htmlpage):
    htmlpage.javascript_src.extend(js_files)
    htmlpage.style_sheets.extend(css_files)

class MessageLikes(object):

    def __init__(self, message):
        self.conf = conf.getInstance()
        self.db   = db.getInstance()

        self.message = message
        self._likes = None

    def toggle(self, user_id):
        if user_id not in [r['user_id'] for r in self.likes]:
            self.add(user_id)
        else:
            self.remove(user_id)

    def add(self, user_id):
        sql = 'insert into likes (user_id, message_id) values (%s, %s)'
        self.db.execute(sql, params=(user_id, self.message.id))
        self._likes = None # reinit likes

    def remove(self, user_id):
        sql = 'delete from likes where user_id = %s and message_id = %s'
        self.db.execute(sql, params=(user_id, self.message.id))

        sql = 'insert into unlikes (user_id, message_id) values (%s, %s)'
        self.db.execute(sql, params=(user_id, self.message.id))

        self._likes = None # reinit likes

    @property
    def num_likes(self):
        return len(self.likes)

    @property
    def likes(self):
        if self._likes is None:
            sql_file = '%s/sql/templates/message_likes.sql' % self.conf.basedir
            sql = open(sql_file, 'r').read()
            self._likes = []
            for row in self.db.query(sql, params=(self.message.id,)):
                self._likes.append({'id'        : row['id'],
                                    'user_id'   : row['user_id'],
                                    'user_fullname': row['user_fullname'],
                                    'message_id': row['message_id']})
        return self._likes

    def html_widget(self, user):
        status_class = 'open'
        if self.num_likes:
            like_icon_file = 'images/thumbs-up2.png'
            likers_link = a(str(self.num_likes),
                            onclick="javascript: toggleLikers('likers_%s')"
                            % self.message.id)
            #if str(user.id) in self.likes:
            #    status_class = 'liked'
        else:
            like_icon_file = 'images/thumbs-up.png'
            likers_link = '0'

        like_icon = img(src=like_icon_file,
                        id='like_icon_%s' % self.message.id)

        like_link = a(like_icon,
                      onclick="javascript: toggleLike(%s)"
                      % self.message.id)

        like_button = span(like_link,
                           title='I like this',
                           id='like_%s' % self.message.id,
                           class_=status_class)
        return span(like_button + likers_link,
                    class_='messageFooterButton')

    def html_likersSection(self):
        desc = p('Liked by:')
        likers = ', '.join([b(n['user_fullname']) for n in self.likes])
        return div(desc + likers, class_='likers', id='likers_%s'
                   % self.message.id)


if __name__ == '__main__':
    # test
    from messages import Message
    m = Message(71)

    ml = MessageLikes(m)
    print ml.num_likes
    print ml.likes[0]['user_fullname']

    ml.add(3)
    print ml.likes[-1]['user_fullname']
