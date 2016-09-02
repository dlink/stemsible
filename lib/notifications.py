from jinja2 import Template
from datetime import datetime, timedelta
from encryptint import encrypt_int

from vlib import db, conf
from vlib.utils import format_datetime
from vweb.html import *

from users import Users, User
from messages import Messages
from emails import Emails
from comments import Comment
from images import getUserImage

NUM_DAYS_BACK = 2

class Notifications(object):

    def __init__(self):
        self.conf = conf.getInstance()
        self.db = db.getInstance()
        self.users = Users()
        self.messages = Messages()
        self.email = Emails()

    def sendMessageActivity(self, user=None):
        '''Given a User Object, or None for all,
           Send Message Activity Email to user(s)

           Send notification about Comments on Users message
           Since the last time run

           TO DO: Implement dynamtic send interval based
                  on number of likes and comments
        '''
        data = self._getMessageComments(user.id if user else None)
        for user_id in data.keys():
            user = User(user_id)
            print 'Email to:', data[user_id]['email']

            posts = []
            for message in data[user_id]['messages']:

                # comments data
                comments = []
                for i, cid in enumerate(message['comment_ids']):
                    cUser = User(Comment(cid).user_id)
                    profile_url = 'http://%s/profile.py?u=%s' % \
                                  (self.conf.baseurl, encrypt_int(cUser.id))
                    comments.append({'name': cUser.fullname,
                                     'profile_image': getUserImage(cUser.id),
                                     'profile_url': profile_url,
                                     'text': message['comment_texts'][i]})
                # activity message
                message_url = 'http://%s/main.py#message_card_%s' \
                              % (self.conf.baseurl, message['id'])
                post_link = a(b('post'), href=message_url)
                activity_msg = '%s new comment%s on your %s' % \
                               (len(comments),
                                's' if len(comments) > 1 else '',
                                post_link)
                posts.append({
                    'activity_msg': activity_msg,
                    'comments': comments,
                    'message_url': 'http://%s/main.py#message_card_%s' \
                           % (self.conf.baseurl, message['id'])
                })

            html = open('%s/lib/emails/message_activity.html' % \
                        self.conf.basedir).read()
            html = Template(html)
            html = html.render(posts=posts)
            self.email.send_email(#to='dvlink@gmail.com',
                                  to=user.email,
                                  subject='Recent activity',
                                  body='',
                                  html=html)

            # update likes and comments as 'notified':
            for message in data[user_id]['messages']:
                for cid in message['comment_ids']:
                    Comment(cid).updateRows({'notification': datetime.now()})

    def _getMessageComments(self, user_id):
        '''Return the following message activity Data structure:

           {1: # user_id
               {'email': 'david@stemsible.com',
               {'messages':
                   [{id: 806,  # message_id
                     'text': "I'm very excited about how Stemsible",
                     'created': <datetime>
                     'comment_ids: [109, 134]
                     'comment_texts': ['test comment message',
                                       'another test comment message']
                   ]}
               }
           }
        '''
        data = {}

        # get sql
        user_filter = 'and u.id = %s' % user_id if user_id else ''
        sql_file = '%s/lib/sql/message_comments.sql' % self.conf.basedir
        sql = open(sql_file, 'r').read() % user_filter

        # loop thru records, tally on user_id change
        for row in self.db.query(sql):

            user_id = row['user_id']
            user_email = row['user_email']
            message_id = row['message_id']
            comment_ids = row['comment_ids'].split(',')
            comment_texts = row['comment_texts'].split('^!^!^')

            if user_id not in data:
                data[user_id] = {'email': user_email,
                                 'messages': []}

            data[user_id]['messages'].append(
                {'id': message_id,
                 #'text': message_text,
                 #'created': message_created,
                 'comment_ids': comment_ids,
                 'comment_texts': comment_texts
                })

        return data


    def sendSummary(self, user=None):
        '''Given a User Object, or None for all,
           Send Summary Email to user(s).
        '''
        # one or all users?
        users = [user] if user else Users().getUsers('1=1')

        time_since = datetime.now() - timedelta(NUM_DAYS_BACK)
        for user in users:
            print 'user:', user
            total_posts = self._getInterestingPosts(user_id=user.id,
                                                    created_after=time_since)
            total_comments = self._getTotalComments(user_id=user.id,
                                                    created_after=time_since)
            total_likes = self._getTotalLikes(user_id=user.id,
                                              created_after=time_since)
            posts = []
            for p in total_posts:
                posts.append({
                    'created': format_datetime(p['last_updated']),
                    'text': ' '.join(p['text'].split(' ')[0:80]), # 80 words
                    'name': p['author'],
                    'profile_image': getUserImage(p['user_id']),
                    'message_url': 'http://%s/main.py#message_card_%s' \
                           % (self.conf.baseurl, p['message_id'])
                })

            html = open('%s/lib/emails/summary.html' %self.conf.basedir).read()
            html = Template(html)
            html = html.render(likes=total_likes, comments=total_comments,
                               posts=posts, plength=len(posts))
            print html
            self.email.send_email(to=user.email,
                                      subject='While you were away',
                                      body="",
                                      html=html)

    def _getTotalLikes(self, user_id, created_after):
        '''Get total likes after 'created_after' on all the posts of a user.
        Given a user_id of type integer and a created_after of type datetime,
        return the total number of likes as integer.
        '''
        sql_file = '%s/sql/templates/email_total_likes.sql' %self.conf.basedir
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
    #Notifications().sendSummary(user)
