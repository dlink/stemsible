#!/usr/bin/env python

import os
from copy import copy

from passlib.hash import sha256_crypt

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
        self.javascript_src.extend(['js/profile.js', 'js/signup.js',
                                    'js/tags.js'])
        self.javascript_src.extend(self.schoolInfo.getJsFile())
        self.cannot_read_profile = 0

        self.missing_fields = []
        self.pw_error_msg = ''
        self.pw_updated = 0

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

        # change schools
        self.schoolInfo.process(self.session, self.form)

        # change profile image
        if 'filename' in self.form and self.user.id == self.session.user.id:
            self._handleImageUpload()

        # change pw
        if 'submit-change-pw' in self.form and \
           self.user.id == self.session.user.id:
            self._processChangePW()

    def _getBody(self):
        if self.cannot_read_profile:
            return self.cannotReadProfile()

        # allow post new message on profile?
        newcard = ''
        if self.user.id == self.session.user.id:
            newcard = self.feed.getNewMessageCard()

        no_posts_msg = ''
        feed = self.feed.getMessages(self.user.id)
        if 'messageCard' not in feed:
            no_posts_msg = div(
                'Looks like %s has not posted anything on Stemsible yet. '
                'Remind them to not be so shy next time you see them.'
                % self.user.first_name,
                style="width: 80%; margin: 20px auto; font-size: 1.3em;")

        # do right before left in order to get self.feed.num_messages
        right = \
            self.schoolInfo.getHtml(self.user) + \
            h3('Posts') + \
            newcard + \
            no_posts_msg + \
            feed

        left = \
            self._getUserData() + \
            self._getChangePW() + \
            self._getPostStats() + \
            self._getUserReachInfo()

            #self._getUserReachInfo2()
            #self._getFollowingInfo()

        return open('profile-section.html', 'r').read() % (left, right)

    def cannotReadProfile(self):
        return center(div(
            h4("We've got a problem.") +\
            p('Sorry we can not read profile')))

    def _handleImageUpload(self, resize=True):
        saveUserImage(self.session.user.id, self.form['filename'].file)

    def _processChangePW(self):
        # set instance values and check missing fields
        for field in ['current_pw', 'password1', 'password2']:
            if field in self.form and self.form[field].value:
                setattr(self, field, self.form[field].value)
            else:
                self.missing_fields.append(field)
                setattr(self, field, '')

        if self.missing_fields:
            self.pw_error_msg += p('Please fill in all fields', class_='red')

        # check current passord
        if self.current_pw and not sha256_crypt.verify(self.current_pw,
                                                       self.user.password):
            self.pw_error_msg += p('Incorrect current password', class_='red')
            self.missing_fields.append('current_pw')

        # check passwords match
        if self.password1 and self.password2 and \
           self.password1 != self.password2:
            self.pw_error_msg += p('Passwords do not match', class_='red')
            self.missing_fields.append('password1')
            self.missing_fields.append('password2')

        # all good - update pass
        if not self.pw_error_msg:
            self.user.update('password', sha256_crypt.encrypt(self.password1))
            self.pw_updated = 1

    def _getUserData(self):
        '''Return User Data Fields as HTML'''
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
        data = [['Name:'  , self.user.fullname]]
        if self.user.id == self.session.user.id:
            data.append(['Email:' , self.user.email])
        data.append([nobr('Member Since:'), format_date(self.user.created)])
        
        # build html table
        table = HtmlTable(class_='profileTable')
        for row in data:
            row_header = span(row[0], class_='profileRowHeader')
            value      = row[1]
            table.addRow([row_header, value])
        table.setColVAlign(1, 'top')

        return header + image + table.getTable()

    def _getChangePW(self):
        '''Return Change Password UX as HTML'''

        if self.user.id != self.session.user.id:
            return ''

        def getFieldClass(field):
            '''Return input field class(es) -add missing-value class if nec.'''
            class_ = 'form-control'
            if field in self.missing_fields:
                class_ += ' missing-value'
            return class_

        # link
        change_pw_link = a('Change Password', class_='btn btn-default btn-sm',
                           id='change-pw-link')

        # user_msg
        user_msg = ''
        if self.pw_updated:
            user_msg = p('Password Updated', style='color: green')
        else:
            user_msg = self.pw_error_msg

        # fields
        class_ = getFieldClass('current_pw')
        current_pw = div(input(type='password',
                               name='current_pw',
                               class_=class_,
                               placeholder='Current Password',
                               value=getattr(self, 'current_pw', '')),
                         class_='form-group')

        class_ = getFieldClass('password1')
        password1  = div(input(type='password',
                               name='password1',
                               class_=class_,
                               id='password1-input',
                               placeholder='New Password',
                               value=getattr(self, 'password1', '')) + \
                         span('', id='passstrength'),
                         class_='form-group')

        class_ = getFieldClass('password2')
        password2 = div(input(type='password',
                              name='password2',
                              class_=class_,
                              id='password2-input',
                              placeholder='Confirm New Password',
                              value=getattr(self, 'password2', '')) + \
                        span('', id='passmatch'),
                        class_='form-group')

        submit = input (type='submit',
                        name='submit-change-pw',
                        class_='form-control btn btn-primary',
                        value='Reset Password')
        fields = div(current_pw + password1 + password2 + submit,
                     id='change-pw-fields')

        style = "display: none" if not self.pw_error_msg else ''
        cpw_form = form(fields, id='change-pw-form', action='/profile.py',
                        style=style)
        return div(change_pw_link + user_msg + cpw_form, id='change-pw')

    def _getPostStats(self):
        '''Return a table of Posting statistics as HTML'''

        table = HtmlTable(class_='profileTable')
        table.addHeader(['Posts', 'Member</br>Reach', 'School<br/>Reach',
                          'Following'])

        # school reach
        school_reach = []
        for f in self.user.followers:
            for s in f.schools:
                school_reach.append(s['school'])
        school_reach = set(school_reach)

        table.addRow([str(self.feed.num_messages),
                       str(len(self.user.followers)),
                       str(len(school_reach)),
                       str(len(self.user.following))])
        table.setRowVAlign(1, 'bottom')
        table.setCellAlign(2, 1, 'center')
        table.setCellAlign(2, 2, 'center')
        table.setCellAlign(2, 3, 'center')
        table.setCellAlign(2, 4, 'center')

        return table.getTable()

    def _getUserReachInfo(self):
        '''Return A list of User Reach Info by School, as HTML'''

        header = p('Schools Reached', id='school-header')

        schools = {}
        for f in self.user.following:
            for s in f.schools:
                name = s['school']
                #if s['state']:
                #    name += ', ' + s['state']
                if name not in schools:
                    schools[name] = 0
                schools[name] += 1

        o = ''
        for name in sorted(schools.keys()):
            name2 = name.replace("'", "\\\'")
            name_link = span(name, onclick="javascript:search('%s')" % name2,
                             class_='cursor-pointer')
            o += li(p('%s - %s' % (name_link, schools[name]),
                      class_='schoolName'))

        return div(header + o, id='school-panel')

    '''
    def _getUserReachInfo2(self):
        header = h3('Schools Reached')

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
    '''

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
