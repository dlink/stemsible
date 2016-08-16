#!/usr/bin/env python

from vweb.html import *

from base import Base

class Forgot_password(Base):

    @property
    def name(self): return 'Forgot_password'

    def __init__(self):
        Base.__init__(self)
        self.require_login = False

    def _getBody(self):
        return open('forgot.html', 'r').read()

if __name__ == '__main__':
    Forgot_password().go()
