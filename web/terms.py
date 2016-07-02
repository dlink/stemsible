#!/usr/bin/env python

from vweb.html import *

from base import Base

class Terms(Base):

    @property
    def name(self): return 'terms'

    def __init__(self):
        Base.__init__(self)
        self.style = '''
.text {
   margin: 30px 100px;
}
'''

    def _getBody(self):
        text = \
            h2('Terms and Conditions') + \
            p('Yet to be determined.')
        return div(text, class_='text')

if __name__ == '__main__':
    Terms().go()
