#!/usr/bin/env python

from vweb.html import *

from base import Base

class Help(Base):

    @property
    def name(self): return 'help'

    def __init__(self):
        Base.__init__(self)
        self.style = '''
.text {
   margin: 30px 100px;
}
'''

    def _getBody(self):
        text = \
            h3('Help') +\
            p('Soon to come')
        return div(text, class_='text')

if __name__ == '__main__':
    Help().go()
