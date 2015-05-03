#!/usr/bin/env python

from vweb.html import *
from vweb.htmlpage import HtmlPage

class Main(HtmlPage):
    
    def __init__(self):
        HtmlPage.__init__(self, 'Stemsible')

    def getHtmlContent(self):
        return p('Stemsible')

if __name__ == '__main__':
    Main().go()

