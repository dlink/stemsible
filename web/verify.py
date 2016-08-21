#!/usr/bin/env python

from vlib import conf
from vweb.html import *

from base import Base

class Verify(Base):

    @property
    def name(self): return 'verify'

    def __init__(self):
        Base.__init__(self)
        #self.style_sheets.extend(['css/home.css'])

        self.conf = conf.getInstance()

        self.verified = False

        self.require_login = False

    def process(self):
        Base.process(self)
        if 't' in self.form:
            token = self.form['t'].value
            self.verified = self.emails.verify_email_token(token)

    def _getBody(self):
        if self.verified:
            return open('verification_success.html', 'r').read()
        return open('verification_fail.html', 'r').read()


if __name__ == '__main__':
    Verify().go()
