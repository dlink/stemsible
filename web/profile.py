#!/usr/bin/env python
from copy import copy

from vlib import conf
from vlib.utils import format_date
from vweb.html import *
from vweb.htmltable import HtmlTable
from vlib.odict import odict

from users import User
from encryptint import encrypt_int, decrypt_int

from base import Base
from feed import Feed
from schoolinfo import SchoolInfo

class Profile(Base):

    @property
    def name(self): return 'profile'

    def __init__(self):
        Base.__init__(self)
        self.conf = conf.getInstance()
        self.feed = Feed(self)
        self.schoolInfo = SchoolInfo()
        self.style_sheets.extend(['css/profile.css', 'css/feed.css'])
        self.style_sheets.extend(self.schoolInfo.getCssFile())
        self.javascript_src.extend(['js/signup.js'])
        self.javascript_src.extend(self.schoolInfo.getJsFile())
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
            
        self.schoolInfo.process(self.session, self.form)

    def _getBody(self):
        if self.cannot_read_profile:
            return self.cannotReadProfile()

        # allow post new message on profile?
        newcard = ''
        if self.user.id == self.session.user.id:
            newcard = self.feed.getNewMessageCard()

        # do right before left in order to get self.feed.num_messages
        right = \
            self.schoolInfo.getHtml(self.user) + \
            h3('Posts') + \
            newcard + \
            self.feed.getMessages(self.user.id)

        left = \
            self._getGeneralInfo() + \
            self._getFollowingInfo()

        o = open('profile-section.html', 'r').read() % (left, right)
        return form(o, name='form1', method='POST')

    def cannotReadProfile(self):
        return center(div(
            h4("We've got a problem.") +\
            p('Sorry we can not read profile')))

    def _getGeneralInfo(self):
        header = h3('Profile')
        # build data
        data = [
            ['Name:'  , self.user.fullname],
            ['Email:' , self.user.email],
            [nobr('Member Since:'), format_date(self.user.created)],
            ['&nbsp;', '&nbsp;']]
        
        # build html table
        table = HtmlTable(class_='profileTable')
        for row in data:
            row_header = span(row[0], class_='profileRowHeader')
            value      = row[1]
            table.addRow([row_header, value])
        table.setColVAlign(1, 'top')

        table2 = HtmlTable(class_='profileTable')
        table2.addHeader(['Posts', 'Followers', 'Following'])
        table2.addRow([str(self.feed.num_messages),
                      str(len(self.user.followers)),
                      str(len(self.user.following))])

        return header + table.getTable() + table2.getTable()

    def _getFollowingInfo(self):
        header = h3('Following')
        '''
        table = HtmlTable(class_='profileTable')
        table.addHeader(['Posts', 'Followers', 'Following'])
        table.addRow([str(self.feed.num_messages),
                      str(len(self.user.followers)),
                      str(len(self.user.following))])
        return header + table.getTable()

        '''
        table = HtmlTable(class_='profileTable')
        data = []
        followings = []
        for f in self.user.following:

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
            schools = span(br().join([s['school'] for s in f.schools]),
                           class_='smaller-text')
            table.addRow([name_link + br()+ schools])

        return header + table.getTable()

if __name__ == '__main__':
    Profile().go()
