#!/usr/bin/env python

from vweb.html import *

from base import Base

class Privacy(Base):

    @property
    def name(self): return 'about'

    def __init__(self):
        Base.__init__(self)

    def _getBody(self):
        return open('privacy.html', 'r').read()

if __name__ == '__main__':
    Privacy().go()
