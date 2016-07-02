#!/usr/bin/env python

from vweb.html import *

from base import Base

class About(Base):

    @property
    def name(self): return 'about'

    def __init__(self):
        Base.__init__(self)
        self.style = '''
.text {
   margin: 30px 100px;
}
'''

    def _getBody(self):
        text = \
            h3('About') +\
            p('Uday Kumar is an entrepreneurs living and working in the D.C. area, and has being working in the online education space for many years.') +\
            p('While many social media platforms exist, Uday recognized that none existed for the parents of children in school.   That was the inspiration for Stemsible') +\
            p('When Uday approached David Link, a computer engine who also has worked in the educational space, he immediately liked the idea and started to build it - and Stemsible was created')
        
        return div(text, class_='text')

if __name__ == '__main__':
    About().go()
