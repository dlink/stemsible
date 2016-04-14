#!/usr/bin/env python

from vlib.utils import format_date
from vweb.html import *
from vweb.htmltable import HtmlTable
from vlib.odict import odict

from base import Base
from feed import Feed

class Profile(Base):

    @property
    def name(self): return 'profile'

    def __init__(self):
        Base.__init__(self)
        self.feed = Feed(self)
        self.style_sheets.append('css/profile.css')
        self.debug_cgi = 0

    def process(self):
        Base.process(self)
        self.feed.process()

    def _getBody(self):
        left = ''
        center = \
            self._getProfileUserHeader() + \
            self._getGeneralInfo()
        right = self._getProfilePostsHeader() + \
                self.feed.getNewMessageCard() + \
                self.feed.getMessages()

        return open('profile-section.html', 'r').read() % (left, center, right)

    def _getProfileUserHeader(self):
        return h3('My Profile')

    def _getGeneralInfo(self):
        table = HtmlTable(class_='profileTable')
        data = [
            ['Name'  , self.session.user.fullname],
            ['Email' , self.session.user.email],
            ['Member Since', format_date(self.session.user.created)],
            ]

        #followers
        followings = []
        for i, f in enumerate(self.session.user.following):
            row_header = 'Following' if i == 0 else ''

            # append (n) to duplicate Usernames
            fullname = f.fullname
            n = 2
            while fullname in followings:
                fullname = '%s (%s)' % (f.fullname, n)
                n += 1
            followings.append(fullname)

            data.append([row_header, fullname])

        for row in data:
            row_header = span(row[0], class_='profileRowHeader')
            value      = row[1]
            table.addRow([row_header, value])
        table.setColVAlign(1, 'top')
        return table.getTable()

    def _getProfilePostsHeader(self):
        return h3('My Posts')

if __name__ == '__main__':
    Profile().go()
