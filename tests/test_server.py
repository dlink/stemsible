#!/usr/bin/env python

from datetime import datetime

import urllib
import urllib2
import unittest

import json

from vlib.odict import odict

# Fixtures

SERVER_URL = 'http://localhost:5000'

ID = 1
EMAIL = 'dvlink@gmail.com'
FIRST_NAME = 'David'
LAST_NAME = 'Link'
FULLNAME = 'David Link'
CREATED = 'Mon, 04 May 2015 20:54:00 GMT'
URI = 'http://localhost:500/users/1'

MESSAGE_ID = 1
MESSAGE_USER_ID = 1
MESSAGE_TEXT = 'Hello There.'
MESSAGE_CREATED = 'Sun, 05 Apr 2015 21:18:00 GMT'
MESSAGE_USER_FULLNAME = 'David Link'


class TestServer(unittest.TestCase):
    '''Test REST Server'''

    def test_REST_getUser(self):
        url = '%s/users/%s' % (SERVER_URL, ID)
        response = urllib2.urlopen(url).read()
        user = odict(json.loads(response))

        self.assertEqual(user.id, ID)
        self.assertEqual(user.first_name, FIRST_NAME)
        self.assertEqual(user.last_name, LAST_NAME)
        self.assertEqual(user.fullname, FULLNAME)
        self.assertEqual(str(user.created), CREATED)

    def test_REST_getUsers(self):
        url = '%s/users' % (SERVER_URL)
        response = urllib2.urlopen(url).read()
        users = odict(json.loads(response)).users

        user1 = odict(users[0])
        self.assertEqual(user1.id, ID)
        self.assertEqual(user1.fullname, FULLNAME)
        self.assertEqual(user1.created, CREATED)
        self.assertEqual(user1.uri, URI)

    def test_REST_getMessage(self):
        url = '%s/messages/%s' % (SERVER_URL, MESSAGE_ID)
        response = urllib2.urlopen(url).read()
        message = odict(json.loads(response))

        self.assertEqual(message.id, MESSAGE_ID)
        self.assertEqual(message.user_id, MESSAGE_USER_ID)
        self.assertEqual(message.text, MESSAGE_TEXT)
        self.assertEqual(message.created, MESSAGE_CREATED)

    def test_REST_getMessageUser(self):
        url = '%s/messages/%s' % (SERVER_URL, MESSAGE_ID)
        response = urllib2.urlopen(url).read()
        message = odict(json.loads(response))

        self.assertEqual(message.user['id'], MESSAGE_USER_ID)
        self.assertEqual(message.user['fullname'], MESSAGE_USER_FULLNAME)

    def test_REST_getMessageFail(self):
        url = '%s/messages/%s' % (SERVER_URL, 0)
        with self.assertRaises(urllib2.HTTPError):
            response = urllib2.urlopen(url).read()

if __name__ == '__main__':
    unittest.main()
