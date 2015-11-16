#!/usr/bin/env python

from vlib.utils import format_date
from vweb.html import *
from vweb.htmltable import HtmlTable

from base import Base

class Welcome(Base):

    def __init__(self):
        Base.__init__(self)
        self.require_login = False

    def process(self):
        Base.process(self)

    def _getBody(self):
        left = ''
        center = \
            h1('Welcome to Stemsible') + \
            p('You should receive an email shortly at X, with a link that '
              'will complete the registration process.')
        right = ''

        return open('body-section.html', 'r').read() % (left, center, right)    

if __name__ == '__main__':
    Welcome().go()
