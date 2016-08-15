#!/usr/bin/env python

import os
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
from images import getUserImage, saveUserImage

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
        self.javascript_src.extend(['js/tags.js'])
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

        if 'filename' in self.form and self.user.id == self.session.user.id:
            self._handleImageUpload()

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
            self._getUserReachInfo2()

            #self._getUserReachInfo() + \
            #self._getFollowingInfo()

        return open('profile-section.html', 'r').read() % (left, right)

    def cannotReadProfile(self):
        return center(div(
            h4("We've got a problem.") +\
            p('Sorry we can not read profile')))

    def _handleImageUpload(self, resize=True):
        saveUserImage(self.session.user.id, self.form['filename'].file)

    def _getGeneralInfo(self):
        header = h3('Profile')
        image_ = div(img(width='150px', src=getUserImage(self.user.id)))

        if self.user.id == self.session.user.id:
            file = input(type='file', name='filename', accept='image/*',
                         onchange='upload_form.submit();')
            browse = span(image_ + file, class_='btn btn-file')
            image = form(browse, enctype='multipart/form-data', action='',
                             method='post', name='upload_form')
        else:
            image = image_

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

        return header + image + table.getTable() + table2.getTable()


    '''
    def _getUserReachInfo(self):
        header = h3('Schools Reached')

        schools = {}
        for f in self.user.following:
            for s in f.schools:
                name = s['school']
                if name not in schools:
                    schools[name] = 0
                schools[name] += 1

        o = ''
        for name in sorted(schools.keys()):
            name2 = name.replace("'", "\\\'")
            name_link = span(name, onclick="javascript:search('%s')" % name2,
                             class_='cursor-pointer')
            o += p('%s - %s' % (name_link, schools[name]))

        return header + o
    '''

    def _getUserReachInfo2(self):
        header = h3('Schools Reached-2')

        schools = {}
        for f in self.user.following:
            for s in f.schools:
                name = s['district']
                if name not in schools:
                    schools[name] = 0
                schools[name] += 1

        o = ''
        for name in sorted(schools.keys()):
            name2 = name.replace("'", "\\\'")
            name_link = span(name, onclick="javascript:search('%s')" % name2,
                             class_='cursor-pointer')
            o += p('%s - %s' % (name_link, schools[name]))

        return header + o

    def _getFollowingInfo(self):
        header = h3('Following')

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
