from users import Users
from messages import Messages
from emails import Emails

from vlib import db, conf
from vlib.utils import format_datetime
from jinja2 import Template
from datetime import datetime, timedelta
import json

from images import getUserImage

NUM_DAYS_BACK = 1

class Notifications(object):

    def __init__(self):
        self.conf = conf.getInstance()
        self.db = db.getInstance()
        self.users = Users()
        self.messages = Messages()
        self.email = Emails()

    def emailNotification(self, user=None):
        '''Given a user as a User Object, Send them an email notifications.
           Collect stats of last 24 hours and send email.

           Send to all users if no user is passed in
        '''
        # one or all users?
        if not user:
            users = Users().getUsers('1=1')
        else:
            users = [user]

        time_since = datetime.now() - timedelta(NUM_DAYS_BACK)
        for user in users:
            print 'user:', user
            total_posts = self._getInterestingPosts(user_id=user.id,
                                                    created_after=time_since)
            total_comments = self._getTotalComments(user_id=user.id,
                                                    created_after=time_since)
            total_likes = self._getTotalLikes(user_id=user.id,
                                              created_after=time_since)
            html = open('%s/lib/email.html' % self.conf.basedir).read()
            posts = []
            for p in total_posts:
                posts.append({
                    'created': format_datetime(p['last_updated']),
                    'text': ' '.join(p['text'].split(' ')[0:80]), # 80 words
                    'name': p['author'],
                    'profile_image': getUserImage(p['user_id'])
                })

            html = Template(html)
            html = html.render(likes=total_likes, comments=total_comments,
                               posts=posts, plength=len(posts))
            self.email.send_email(to=user.email,
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
        sql_file = '%s/sql/templates/email_total_comments.sql' \
                   % self.conf.basedir
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
        resp = self.db.query(sql, params=[user_id])
        return resp

if __name__ == '__main__':
    import sys
    email = sys.argv[1]
    user = Users().getUsers({'email': email})[0]
    Notifications().emailNotification(user)
