#!/usr/bin/env python

from vweb.html import *
from vweb.htmlpage import HtmlPage

from header import Header

class Main(HtmlPage):
    
    def __init__(self):
        HtmlPage.__init__(self, 'Stemsible')
        self.header = Header('Stemsible')

    def getHtmlContent(self):
        return \
            self.header.getHtml() + \
            self._getBody() + \
            self._getFooter()

    def _getBody(self):
        return p('Body')

    def _getFooter(self):
        return p('Footer')

if __name__ == '__main__':
    Main().go()

