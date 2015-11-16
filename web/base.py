#!/usr/bin/env python

import os

from vlib.utils import lazyproperty
from vweb.html import *
from vweb.htmlpage import HtmlPage

from session import Session, SessionErrorLoginFail

USER_CHOOSER = 0 # turning on needs rework with new login mech.

class Base(HtmlPage):

    @lazyproperty
    def users(self):
        from users import Users
        return Users()

    def __init__(self, name='Stembsible'):
        HtmlPage.__init__(self, name) #, include_form_tag=0)
        self.style_sheets = [
            'bootstrap/css/bootstrap.min.css',
            'http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/css/' \
                'bootstrap-combined.min.css',
            'css/app.css']
        self.javascript_src.extend([
                "//code.jquery.com/jquery-1.10.2.js",
                "//code.jquery.com/ui/1.11.1/jquery-ui.js",
                'bootstrap/js/bootstrap.min.js'])
        if USER_CHOOSER:
            self.style_sheets.append('css/userchooser.css')
        self.isSubstituteUser = False
        self.debug_cgi = 0
        self.require_login = True

    def process(self):
        HtmlPage.process(self)
        self._processSession()

        # substitute user
        #   this needs rework for new login mech
        #self.actual_user = self.session.user.id
        if 'user_chooser' in self.form:
            self.user = User(self.form['user_chooser'].value)
            self.isSubstituteUser = True

    def _processSession(self):
        # get session
        self.session = Session()

        # set HtmlPage cookie:
        self.cookie = str(self.session.cookie)

        # logging out?
        if 'logout' in self.form:
            self.session.logout()

        # logging in?
        if 'login_submit' in self.form and 'email' in self.form \
                and 'password' in self.form:
            try:
                self.session.login(self.form['email'].value,
                                   self.form['password'].value)
            except SessionErrorLoginFail, e:
                self.debug_msg += p(str(e))

        # close session
        self.session.close()

        # need to be logged in?
        if self.require_login and not self.session.logged_in:
            print 'Location: login.py'

    def getHtmlContent(self):
        return \
            self._getHeader() + \
            self._getBody() + \
            self._getFooter()

    def _getHeader(self):

        if self.session.logged_in:
            profile_button = input(name='profile', class_='btn btn-info btn-xs',
                                   type='button',
                                   value=space_pad(self.session.user.fullname),
                                   onclick="location.href='profile.py';")
            logout = input(name='logout', class_='btn btn-xs',
                           type='submit', value=space_pad('Logout'))
            welcome = 'Welcome %s' % profile_button
            action = '&nbsp;' + logout
        else:
            welcome = ''
            action = ''

        return open('header-section2.html', 'r').read() % \
            (welcome, action) # self._getUserChooser())

    def _getBody(self):
        return open('body-section.html', 'r').read() % (
            p('this is the base class'))

    def _getUserChooser(self):
        '''Used for debug
           provide a drop down of different users
        '''
        if not USER_CHOOSER:
            return ''

        options = ''
        for id, username in self.users.getUserMap():
            if id == self.user.id:
                options += option(username, value=id, selected='1')
            else:
                options += option(username, value=id)
        return select(options, name='user_chooser', id='user_chooser',
                      onChange='submit()', class_='selectpicker')


    def _getFooter(self):
        # not op
        return ''

        items = ['FAQ', 'About', 'Terms & Privacy', 'Contact']
        #links = [a(i, href='/%s' % i) for i in items]
        o = hr()
        for i in items:
            #o += a(i, href='/%s' % i)
            o += span(i, class_='footerLink')
        return div(o, id='footer')

def space_pad(s):
    return '&nbsp; %s &nbsp;' % s

if __name__ == '__main__':
    Base().go()
