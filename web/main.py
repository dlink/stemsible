#!/usr/bin/env python

from vlib.odict import odict

from vweb.html import *
from vweb.htmlpage import HtmlPage

class Main(HtmlPage):

    def __init__(self):
        HtmlPage.__init__(self, 'Stemsible')
        self.style_sheets = ['css/main.css']

    def process(self):
        self.user = odict({'name': 'dlink',
                           'id': 10})

    def getHtmlContent(self):
        return \
            self._getHeader() + \
            self._getBody() + \
            self._getFooter()

    def _getHeader(self):
        # logo/name
        name = span('Stemsible', id='headerName')

        # search bar
        field = input(name='search',
                      size=50,
                      value='Search for activities, answers, and advice')
        search = span(field, id='searchBar')

        # login Info
        href='/user/%s' % self.user.id
        link = a(self.user.name, href=href)
        login_info = span('Logged In as: %s' % link, id='loginInfo')

        return div(
            name +
            search +
            login_info, id='header')

    def _getBody(self):
        o = div(p('hi'), id='messageArea')

        return div(o, id='body')

    def _getFooter(self):
        items = ['FAQ', 'About', 'Terms & Privacy', 'Contact']
        #links = [a(i, href='/%s' % i) for i in items]
        o = hr()
        for i in items:
            o += a(i, href='/%s' % i)
        return div(o, id='footer')

if __name__ == '__main__':
    Main().go()
