from users import Users
from messages import Messages
from emails import Emails

from vlib import db, conf
from jinja2 import Template
from datetime import datetime, timedelta
import json

NUM_DAYS_BACK = 1

class Notifications(object):

    def __init__(self):
        self.conf = conf.getInstance()
        self.db = db.getInstance()
        self.users = Users()
        self.messages = Messages()
        self.email = Emails()

    def emailNotification(self):
        '''Send email notifications. Collect stats of last 24 hours and
           send email.
        '''
        print 'emailNotifications()'
        time_since = datetime.now() - timedelta(NUM_DAYS_BACK)
        users = self.users.getTable()
        for user in users:
            print 'user:'
            total_posts = self._getInterestingPosts(user_id=user['id'],
                                                    created_after=time_since)
            total_comments = self._getTotalComments(user_id=user['id'],
                                                    created_after=time_since)
            total_likes = self._getTotalLikes(user_id=user['id'],
                                              created_after=time_since)
            html = open('email.html').read()
            posts = []
            for p in total_posts:
                u = list(filter(lambda x: x['id']==p['user_id'], users))[0]
                posts.append({
                    'timestamp': p['last_updated'],
                    'text': p['text'],
                    'name': u['first_name'] + " " + u['last_name']
                })
            html = Template(html)
            html = html.render(likes=total_likes, comments=total_comments,
                               posts=posts, plength=len(posts))
            self.email.send_email(to=user['email'],
                                  subject='While you were away',
                                  body="",
                                  html=html)

    def _getTotalLikes(self, user_id, created_after):
        '''Get total likes after 'created_after' on all the posts of a user.
        Given a user_id of type integer and a created_after of type datetime,
        return the total number of likes as integer.
        '''
        sql_file = '%s/sql/templates/email_total_likes.sql' % self.conf.basedir
        sql = open(sql_file, 'r').read()
        resp = self.db.query(sql, params=(user_id, created_after))
        return resp[0]['total_likes']

    def _getTotalComments(self, user_id, created_after):
        '''Get total comments after 'created_after' on all the posts of a user
        Given a user_id of type integer and a created_after of type datetime,
        return the total number of comments as integer.
        '''
        sql_file = '%s/sql/templates/email_total_comments.sql' % self.conf.basedir
        sql = open(sql_file, 'r').read()
        resp = self.db.query(sql, params=(user_id, created_after))
        return resp[0]['total_comments']

    def _getInterestingPosts(self, user_id, created_after):
        '''Get top 5 interesting posts created after 'created_after' for a user
        '''
        # currently, we retrieve only top 5 posts so we do not use user_id
        # or created_after
        sql_file = '%s/sql/templates/email_posts.sql' % self.conf.basedir
        sql = open(sql_file, 'r').read()
        resp = self.db.query(sql)
        return resp
