#!/usr/bin/env python

import os

from vlib.utils import lazyproperty
from vlib import conf
from vweb.html import *
from vweb.htmlpage import HtmlPage

from session import Session, SessionErrorLoginFail

class Base(HtmlPage):

    @lazyproperty
    def users(self):
        from users import Users
        return Users()

    @lazyproperty
    def emails(self):
        from emails import Emails
        return Emails()

    def __init__(self, name='Stemsible'):
        HtmlPage.__init__(self, name, include_form_tag=0)
        self.conf = conf.getInstance()

        self.style_sheets = [
            'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/' \
                'bootstrap.min.css',
            'css/main.css',
            'css/header.css']

        self.javascript_src.extend([
                'https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/' \
                    'jquery.min.js',
                'https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/' \
                    'jquery-ui.min.js',
                'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/' \
                    'bootstrap.min.js',
                'js/header.js',
                ])
        self.debug_cgi = 0
        self.reset_pw_msg = None
        self.require_login = True
        self.user_msg = ''
        self.search = None

    def process(self):
        HtmlPage.process(self)
        self._processSession()

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
                self.user_msg += p(str(e), class_='right user-msg error')

        # close session
        self.session.close()

        # reset password?
        if 'forgot_password_submit' in self.form and 'email-fpw' in self.form:
            email_fpw = self.form['email-fpw'].value
            try:
                self.emails.send_new_password(email_fpw)
                self.reset_pw_msg = p('Okay. Your password was reset. '
                                      'An email was sent to: %s' %
                                      email_fpw, class_='user-msg')
            except Exception, e:
                self.reset_pw_msg =p("Sorry we couldn't reset password. %s" % e,
                                     id='pw-reset-msg', class_='user-msg error')

        # need to be logged in?
        if self.require_login and not self.session.logged_in:
            print 'Location: home.py'

    def getHtmlContent(self):
        o = self._getHeader() + \
            self._getUserMsg() + \
            self._getBody() + \
            self._getFooter()
        return div(o, class_='container')

    def _getHeader(self):
        if self.conf.environment != 'prod':
            sys_ind = font(' (%s)' % self.conf.environment, size=-1)
        else:
            sys_ind = ''


        if not self.session.logged_in:
            on_the_right = self._getLogin() + \
                           self._getPasswordReset()
            return open('header1.html', 'r').read() % (
                sys_ind,
                on_the_right)
        else:
            on_the_right = self._getProfileButton() + \
                           self._getHomeButton() + \
                           self._getHeaderMenu()
            return open('header2.html', 'r').read() % (
                sys_ind,
                self.search or '',
                on_the_right)

    def _getLogin(self):
        # email
        email_label = label('Email',
                            for_='email-input')
        email_field = input(type='email',
                            name='email',
                            class_='form-control input-sm',
                            id='email-input',
                            placeholder="Email")
        email = div(email_label + email_field, class_='form-group')

        # password
        pass_label = label('Password',
                           for_='password-input')
        pass_field = input(type='password',
                           name='password',
                           class_='form-control input-sm',
                           id='password-input',
                           placeholder='Password')
        password = div(pass_label + pass_field, class_='form-group')

        button = input(type='submit',
                       name='login_submit',
                       class_='btn btn-default btn-sm',
                       value='Login')

        return form(email + password + button + self._getForgotPW(),
                    class_='form-inline',
                    action='/home.py')

    def _getForgotPW(self):
        # forgot password
        link = p('Forgot Password?', id='forgotpw-link', class_='clear')

        # header
        header = h3('Forgot Password')

        # text
        text = p("Please enter your email and we'll reset your password.")

        #email
        email_label = ''#label('Email',
                        #    for_='email-input')
        email_field = input(type='email',
                            name='email-fpw',
                            class_='form-control',
                            id='email-input',
                            placeholder="Email")

        button = input(type='submit',
                       name='forgot_password_submit',
                       class_='btn btn-default btn-sm',
                       value='Reset Password')

        fields = div(header + text + email_label + email_field + button,
                     class_='form-group', id='forgotpw-panel')
        forgotPWform = form(fields, class_='form-inline', action='/home.py')

        return link + div(forgotPWform, id='forgotpw')

    def _getPasswordReset(self):
        return self.reset_pw_msg if self.reset_pw_msg else ''
    
    def _getHeaderMenu(self):

        # menu triangle

        menu_triangle = div(div('', class_='arrow-down'),
                            id='header-menu-triangle',
                            onclick='javascript:toggleHeaderMenu()')
        # logout
        logout_option = a('Logout', onclick='javascript:logout()')
        logout_input  = input(type='hidden',
                              name='logout',
                              value='')

        # menu

        options = [['About Stemsible', 'about.py'],
                   ['Help', 'help.py'],
                   ['Terms and Conditions', 'terms.py'],
                   ['Privacy Policy', 'privacy.py'],
                   ['Logout', 'logout']]
        o = ''
        for option, url in options:
            if option == 'Logout':
                o += li(logout_option + logout_input)
            else:
                o += li(a(option, href=url))

        menu = ul(o, id='header-menu')


        return form(menu_triangle + menu,
                    name='header-form',
                    class_='form-inline')

    def _getProfileButton(self):
        welcome = label('Hello',
                        for_='profile-button')
        profile_button = input(type='button',
                               name='profile',
                               id='profile-button',
                               class_='btn btn-xs btn-info',
                               value=self.session.user.fullname,
                               onclick="location.href='profile.py';")
        return welcome + profile_button

    def _getHomeButton(self):
        home_button = input(type='button',
                               name='home',
                               id='home-button',
                               class_='btn btn-xs btn-info',
                               value='Home',
                               onclick="location.href='main.py';")
        return home_button

    def _getUserMsg(self):
        return div(self.user_msg)

    def _getBody(self):
        return open('body-section.html', 'r').read() % (
            p('this is the base class'))

    def _getFooter(self):
        o = ''
        return o

        #items = ['FAQ', 'About', 'Terms & Privacy', 'Contact']
        #o = hr()
        #for i in items:
        #    o += span(i, class_='footerLink')
        #return div(o, id='footer')

if __name__ == '__main__':
    Base().go()
