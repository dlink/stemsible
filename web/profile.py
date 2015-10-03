#!/usr/bin/env python

from vlib.utils import format_date
from vweb.html import *
from vweb.htmltable import HtmlTable

from session import Session

from base import Base

class Profile(Base):

    def __init__(self):
        Base.__init__(self)
        self.style_sheets.append('css/profile.css')
        self.debug_cgi = 0
        self.session = Session()

    def process(self):
        Base.process(self)

    def _getBody(self):
        return open('body-section.html', 'r').read() % (
            '', '',
            self._getProfileHeader() +
            self._getUserFields(),
            '')

    def _getProfileHeader(self):
        return h1('Your User Profile')

    def _getUserFields(self):
        table = HtmlTable(class_='profileTable')
        data = [
            ['Name'  , self.session.user.fullname],
            ['Email' , self.session.user.email],
            ['Member Since', format_date(self.session.user.created)],
            ]

        #followers
        for i, f in enumerate(self.session.user.following):
            if i == 0:
                row_header = 'Following'
            else:
                row_header = ''
            data.append([row_header, f.fullname])

        for row in data:
            row_header = span(row[0], class_='profileRowHeader')
            value      = row[1]
            table.addRow([row_header, value])
        return table.getTable()
    
if __name__ == '__main__':
    Profile().go()
