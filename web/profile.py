#!/usr/bin/env python

from vlib import conf
from vlib.utils import format_date
from vweb.html import *
from vweb.htmltable import HtmlTable
from vlib.odict import odict

from users import User
from encryptint import encrypt_int, decrypt_int

from base import Base
from feed import Feed

class Profile(Base):

    @property
    def name(self): return 'profile'

    def __init__(self):
        Base.__init__(self)
        self.conf = conf.getInstance()
        self.feed = Feed(self)
        self.style_sheets.append('css/profile.css')
        self.cannot_read_profile = 0
        self.debug_cgi = 0

    def process(self):
        Base.process(self)
        self.feed.process()

        # user id passed in
        if 'u' in self.form:
            try:
                id = decrypt_int(self.form['u'].value)
            except Exception, e:
                self.cannot_read_profile = 1
            try:
                self.user = User(id)
            except Exception, e:
                self.cannot_read_profile = 1

        # use loggined in user:
        else:
            self.user = self.session.user

    def _getBody(self):
        if self.cannot_read_profile:
            return self.cannotReadProfile()

        # allow post new message on profile?
        newcard = ''
        if self.user.id == self.session.user.id:
            newcard = self.feed.getNewMessageCard()

        left = ''
        center = \
            self._getProfileUserHeader() + \
            self._getGeneralInfo()
        right = self._getProfilePostsHeader() + \
                newcard + \
                self.feed.getMessages(self.user.id)

        return open('profile-section.html', 'r').read() % (left, center, right)

    def cannotReadProfile(self):
        return center(div(
            h4("We've got a problem.") +\
            p('Sorry we can not read profile')))

    def _getProfileUserHeader(self):
        return h3('Profile')

    def _getGeneralInfo(self):
        # build data
        data = [
            ['Name:'  , self.user.fullname],
            ['Email:' , self.user.email],
            [nobr('Member Since:'), format_date(self.user.created)],
            ['&nbsp;', '&nbsp;']]

        #followers
        followings = []
        for i, f in enumerate(self.user.following):
            row_header = 'Following:' if i == 0 else ''

            # append (n) to duplicate Usernames
            fullname = f.fullname
            n = 2
            while fullname in followings:
                fullname = '%s (%s)' % (f.fullname, n)
                n += 1
            followings.append(fullname)

            # add follower info to data
            name_link = a(fullname, href='//%s/profile.py?u=%s'
                          % (self.conf.baseurl, encrypt_int(f.id)))
            data.append([row_header, name_link])

        # build html table
        table = HtmlTable(class_='profileTable')
        for row in data:
            row_header = span(row[0], class_='profileRowHeader')
            value      = row[1]
            table.addRow([row_header, value])
        table.setColVAlign(1, 'top')
        return table.getTable()

    def _getProfilePostsHeader(self):
        return h3('Posts')

if __name__ == '__main__':
    Profile().go()
