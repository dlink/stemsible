#!/usr/bin/env python

# AJAX Response Handler for Likes
# TODO: Not currently in use.
#       Main Liking functionality needs to switch to AJAX calls and call this

import cgi
import json

from vlib import logger

from messages import Message
from messagelikes import MessageLikes
from session import Session, SessionErrorLoginFail

class Like(object):

    def __init__(self):
        self.logger = logger.getLogger('Like')
        self.response = {'command': 'like'}

    def go(self):
        self.process()
        self.genPage()

    def process(self):
        '''Process Request'''
        self.form        = cgi.FieldStorage()
        error = ''
        try:
            # get user from session
            session = Session()
            session.close()
            if not session.logged_in:
                raise Exception('User not logged in')

            # get mid parameter
            if 'mid' not in self.form:
                raise Exception('mid parameter not in request')

            user_id    = self.response['user_id']    = session.user.id
            message_id = self.response['message_id'] = self.form['mid'].value
            MessageLikes(Message(message_id)).add(user_id)

        except Exception, e:
            error = 'Could not write user/message/like: %s' % e

        # build response
        if error:
            self.response.update({'status': 'fail', 'error': error})
            self.logger.warn(str(self.response))
        else:
            self.response.update({'status': 'success'})
            self.logger.info(str(self.response))

    def genPage(self):
        print 'Content-Type: application/json\n'
        print json.dumps(self.response);

if __name__ == '__main__':
    Like().go()
