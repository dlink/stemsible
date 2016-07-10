#!/usr/bin/env python

from datetime import datetime
import unittest
from record import RecordError

from messages import Message, Messages

# Fixtures

ID = 1
USER_ID = 1
TEXT = 'Hello There.'
USER_FULLNAME = 'David Link'


class TestMessages(unittest.TestCase):
    '''Test Messages'''

    def test_get(self):
        messages = Messages().getMessages()['messages']
        self.assertEqual(messages[-1]['user_id'], USER_ID)

    def test_message(self):
        message = Message(ID)
        self.assertEqual(message.id, ID)
        self.assertEqual(message.user_id, USER_ID)
        self.assertEqual(message.text, TEXT)
        self.assertTrue(isinstance(message.last_updated, datetime))

    def test_messageUser(self):
        message = Message(ID)
        self.assertEqual(message.user.id, USER_ID)
        self.assertEqual(message.user.fullname, USER_FULLNAME)

    def test_messageFail(self):
        with self.assertRaises(RecordError):
            message = Message(0)

if __name__ == '__main__':
    unittest.main()
