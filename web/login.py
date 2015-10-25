#!/usr/bin/env python

from vlib.utils import format_date
from vweb.html import *
from vweb.htmltable import HtmlTable

from base import Base

class Login(Base):

    def __init__(self):
        Base.__init__(self)
        self.style_sheets.append('css/login.css')
        self.require_login = False

    def process(self):
        Base.process(self)
        if self.session.logged_in:
            print 'Location: main.py'

    def _getBody(self):
        table = HtmlTable(class_='mainTable')
        or_cell = p('&nbsp;') + b('or', class_='inactive-text')
        table.addRow([self._getLogin(),
                      or_cell,
                      self._getSignUpNow()])
        table.setRowVAlign(1, 'top')
        return center(table.getTable())

    def _getLogin(self):

        table = HtmlTable(class_='loginTable')
        email_label    = span('Email', class_='loginRowHeader')
        password_label = span('Password', class_='loginRowHeader')
        
        email_field    = input(name='email',    type='text')
        password_field = input(name='password', type='password')

        forgot_password = a('Forgot Password?') + '(coming soon)'

        login_button = input(name='login_submit', class_='btn btn-info',
                             type='submit', value='Login')
        table.addRow([email_label,    email_field])
        table.addRow([password_label, password_field])
        table.addRow([forgot_password])
        table.setCellColSpan(table.rownum, 1, 2)

        table.addRow(['&nbsp;'])
        table.addRow([center(login_button)])
        table.setCellColSpan(table.rownum, 1, 2)

        return center(h4('Login') + table.getTable())
    
    def _getSignUpNow(self):
        table = HtmlTable(class_='loginTable')

        email_label     = span('Email *', class_='inactive-text')
        first_name_label= span('First Name', class_='inactive-text')
        last_name_label = span('Last Name', class_='inactive-text')
        password1_label = span('Password *', class_='inactive-text')
        password2_label = span('Password Confirm*', class_='inactive-text')

        email_field      = input(name='email', disabled=1)
        first_name_field = input(name='first_name', disabled=1)
        last_name_field  = input(name='last_name', disabled=1)
        password1_field  = input(name='password1', type='password', disabled=1)
        password2_field  = input(name='password_confirm', type='password',
                                 disabled=1)

        signup_button = input(name='signup', class_='btn',
                              type='submit', value='Sign Up', disabled=1)

        data = [
            [email_label,      email_field],
            [first_name_label, first_name_field],
            [last_name_label,  last_name_field],
            [password1_label,  password1_field],
            [password2_label,  password2_field],
            ]

        for row in data:
            row_header = span(row[0], class_='loginRowHeader')
            value      = row[1]
            table.addRow([row_header, value])

        table.addRow(['&nbsp;'])
        table.addRow(['* Required fields'])
        table.addRow([center(signup_button)])
        table.setCellColSpan(table.rownum, 1, 2)

        return center(h4('Sign Up Now', class_='inactive-text') + \
                      p('Coming Soon', class_='inactive-text') + \
                      table.getTable())

if __name__ == '__main__':
    Login().go()
