#!/usr/bin/env python

from datetime import datetime
import unittest

from messages import Message

# Fixtures

ID = 1
USER_ID = 1
TEXT = 'Hello There.'
CREATED = '2015-04-05 21:18:00'


class TestMessages(unittest.TestCase):
    '''Test Messages'''

    def test_getMessage(self):
        message = Message(ID)
        self.assertEqual(message.id, ID)
        self.assertEqual(message.user_id, USER_ID)
        self.assertEqual(message.text, TEXT)
        self.assertEqual(str(message.created), CREATED)
        self.assertTrue(isinstance(message.last_updated, datetime))

if __name__ == '__main__':
    unittest.main()
