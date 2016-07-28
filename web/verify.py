#!/usr/bin/env python

from vlib import conf
from vweb.html import *

from base import Base
from emails import Emails


class Verify(Base):

    @property
    def name(self): return 'verify'

    def __init__(self):
        Base.__init__(self)
        self.conf = conf.getInstance()
        self.verified = False
        self.emails = Emails()

        self.require_login = False

    def process(self):
        Base.process(self)
        if 't' in self.form:
            token = self.form['t'].value
            self.verified = self.emails.verify_email_token(token)

    def _getBody(self):
        if self.verified:
            return div('Your email is verified.')
        return div('Something went wrong.')


if __name__ == '__main__':
    Verify().go()
