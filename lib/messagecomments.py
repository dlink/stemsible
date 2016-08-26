import re

from datetime import datetime

from vlib import conf
from vlib import db
from vweb.html import *

from encryptint import encrypt_int, decrypt_int
from jinja2.utils import urlize

from images import getUserImage

js_files = ['js/comments.js']
css_files = ['css/comments.css']


def addHeaders(htmlpage):
    htmlpage.javascript_src.extend(js_files)
    htmlpage.style_sheets.extend(css_files)


class MessageComments(object):

    def __init__(self, message):
        self.conf = conf.getInstance()
        self.db = db.getInstance()

        self.message = message
        self._comments = None

    def toggle(self, user_id):
        if user_id not in [r['user_id'] for r in self.comments]:
            self.add(user_id)
        else:
            self.remove(user_id)

    def add(self, user_id):
        sql = 'insert into comments (user_id, message_id) values (%s, %s)'
        self.db.execute(sql, params=(user_id, self.message.id))
        self._comments = None  # reinit comments

    def remove(self, user_id):
        sql = 'delete from comments where user_id = %s and message_id = %s'
        self.db.execute(sql, params=(user_id, self.message.id))

        sql = 'insert into uncomments (user_id, message_id) values (%s, %s)'
        self.db.execute(sql, params=(user_id, self.message.id))

        self._comments = None  # reinit comments

    @property
    def num_comments(self):
        return len(self.comments)

    @property
    def comments(self):
        if self._comments is None:
            sql_file = '%s/sql/templates/message_comments.sql' \
                % self.conf.basedir
            sql = open(sql_file, 'r').read()
            self._comments = []
            for row in self.db.query(sql, params=(self.message.id,)):
                self._comments.append({'id'        : row['id'],
                                       'user_id'   : row['user_id'],
                                       'user_fullname': row['user_fullname'],
                                       'text'      : row['text'],
                                       'created'   : row['created']})
        return self._comments

    def html_widget(self):
        '''Desided we didn't need a widget - just always show comments'''
        return ''

        """
        status_class = 'open'
        if self.num_comments:
            comment_icon_file = 'images/comment2.png'
        else:
            comment_icon_file = 'images/comment.png'

        onclick = "javascript: toggleComments('comments_%s')" % self.message.id

        num_comments = a(str(self.num_comments),onclick=onclick)

        comments_icon = a(img(src=comment_icon_file), onclick=onclick)

        return span(comments_icon + num_comments,
                    class_='messageFooterButton')
        """

    def html_commentsSection(self, user, search=None):
        comment_cards = []

        # get existing comments
        for comment in self.comments:
            image = getUserImage(comment['user_id'])
            user_icon = div(img(src=image, width='30px',
                            class_='img-thumbnail'),
                            class_='userIcon')
            who = comment['user_fullname']
            text = comment['text']

            if search:
                for term in search.split(' '):
                    text = urlize(text, target='_blank')
                    term2 = r'(%s)' % term
                    text = re.sub(term2, r'<span class="search-term">\1</span>',
                                  text, flags=re.IGNORECASE)

            time_ago = cal_time_ago(comment['created'])
            who_link = a(who, href='//%s/profile.py?u=%s'
                             % (self.conf.baseurl, encrypt_int(comment['user_id'])))
            comment_card = div(span(user_icon) + ' ' +
                               span(who_link, class_='commenter') + ' ' +
                               span(text, class_='comment-text') + ' ' +
                               span(time_ago, class_='comment-time-ago'),
                               class_='comment-card')
            comment_cards.append(comment_card)

        # add new comment field:
        new_comment_card = open('new-comment.html', 'r').read()\
            .format(message_id=self.message.id)
        comment_cards.append(new_comment_card)

        comment_cards_html = '\n'.join(comment_cards)
        return div(comment_cards_html, class_='comments',
                   id='comments_%s' % self.message.id)


def cal_time_ago(date):
    '''Given a datetime
       Return time ago from now in
          form of seconds, minutes, hours or days
          with prefixes of s, m, h and d
    '''
    diff = datetime.now() - date
    days = diff.days

    if days > 0:
        return "%sd" % days

    secs = diff.seconds
    if secs < 60:
        return '%ss' % secs
    elif secs < 60*60:
        return '%sm' % (secs/60)
    else:
        return '%sh' % (secs/60/60)
