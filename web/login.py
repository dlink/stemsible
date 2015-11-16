#!/usr/bin/env python

from vlib.utils import format_date, valid_email
from vweb.html import *
from vweb.htmltable import HtmlTable

from base import Base
from grades import Grades
from registration import Registration
from schoolrelationships import SchoolRelationships

USER_STATUS_PENDING = 8

LOGIN_FIELDS = ['email', 'password']
SIGNUP_FIELDS = ['email1', 'first_name', 'last_name', 'password1','password2']
SCHOOL_FIELDS = ['school_rel1', 'school1', 'grade1']

class Login(Base):

    def __init__(self):
        Base.__init__(self)
        self.style_sheets.extend(['css/login.css', 'css/signup.css'])
        self.javascript_src.extend(['js/typeahead.js', 'js/signup.js'])
        self.require_login = False
        self.su_error_msg = ''
        self.su_missing_fields = []

    def process(self):
        Base.process(self)

        # coming back from a login
        if self.session.logged_in:
            print 'Location: main.py'

        # coming back from a sign up
        if 'signup' in self.form:
            self._processSignUp()

        # init fields
        for f in LOGIN_FIELDS + SIGNUP_FIELDS + SCHOOL_FIELDS:
            setattr(self, f, self.form[f].value if (f in self.form) else '')

    def _getBody(self):
        table = HtmlTable(class_='mainTable')
        or_cell = p('&nbsp;') + b('or', class_='inactive-text')
        table.addRow([self._getLogin(),
                      or_cell,
                      self._getSignUpNow()])
        table.setRowVAlign(1, 'top')

        return center(table.getTable())

    def _getSignUpErrorMsg(self):
        if self.su_error_msg:
            return p(self.su_error_msg, class_='errorMsg')
        else:
            return ''

    def _getLogin(self):
        table = HtmlTable(class_='loginTable')
        email_label    = span('Email', class_='loginRowHeader')
        password_label = span('Password', class_='loginRowHeader')

        email_field    = input(name='email', value=self.email)
        password_field = input(name='password', value=self.password,
                               type='password')

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

        attr = lambda f: {'class_':'red'} if f in self.su_missing_fields else {}

        ### Basic Info

        # labels:
        email_label     = span('Email*'           , **attr('email1'))
        first_name_label= span('First Name*'      , **attr('first_name'))
        last_name_label = span('Last Name*'       , **attr('last_name'))
        password1_label = span('Password*'        , **attr('password1'))
        password2_label = span('Password Confirm*', **attr('password2'))

        # fields:
        email_field      = input30(name='email1', value=self.email1)
        first_name_field = input30(name='first_name', value=self.first_name)
        last_name_field  = input30(name='last_name', value=self.last_name)
        password1_field  = input30(name='password1', value=self.password1,
                                   type='password', id='password1')

        password2_field  = input30(name='password2', value=self.password2,
                                   type='password', id='password2')
        password_strength = span('', id='passstrength')
        password_match    = span('', id='passmatch')

        # build table with basic info
        table = HtmlTable(class_='loginTable')
        data = [
            [email_label,      email_field, ''],
            [first_name_label, first_name_field, ''],
            [last_name_label,  last_name_field, ''],
            [password1_label,  password1_field, password_strength],
            [password2_label,  password2_field, password_match],
            ]

        for row in data:
            label, field, other = row
            row_header = span(label, class_='loginRowHeader')
            value      = field
            table.addRow([row_header, value, other])

        ### School Info

        # header
        table.addRow(['&nbsp;'])
        table.addRow([center('Schools', class_='loginRowHeader'),
                      '',
                      center('Grades', class_='loginRowHeader')])
        table.setCellColSpan(table.rownum, 1, 2)

        # mark missing fields?
        missing_fields = 0
        for field in ['school_rel1', 'school1', 'grade1']:
            if field in self.su_missing_fields:
                missing_fields = 1
                break

        # Fields
        data = []
        for n in [1]: #,2,3,4]: # just show one for now
            r = True if n == 1 else False
            arrow = ''
            if n == 1 and missing_fields:
                arrow = span(b('&#8656;'), class_='red')

            data.append([self._schoolRelField(n, r),
                         self._schoolField(n, r),
                         self._gradeField(n, r) + arrow])
        for i, row in enumerate(data):
            label, field, grade = row
            row_header = span(label, class_='loginRowHeader')
            value      = field
            table.addRow([row_header, value, grade])
            table.setRowVAlign(table.rownum, 'top')

        ### Sign Up button

        signup_button = input(name='signup', class_='btn btn-info',
                              type='submit', value='Sign Up')

        table.addRow(['&nbsp;'])
        table.addRow([center(signup_button)])
        table.setCellColSpan(table.rownum, 1, 3)

        return center(h4('Sign Up Now') +
                      self._getSignUpErrorMsg() +
                      div(table.getTable(), class_='form-group'))

    def _processSignUp(self):
        # check required fields:
        for field in SIGNUP_FIELDS + ['school1']:
            if field not in self.form or not self.form[field].value:
                self.su_missing_fields.append(field)

        # chech required drop down menus
        for field in ['school_rel1', 'grade1']:
            if not int(self.form[field].value):
                self.su_missing_fields.append(field)

        # sign up error message
        if self.su_missing_fields:
            self.su_error_msg += 'Please fill in required fields marked in red'
            return

        # email cool?
        email = self.form['email1'].value
        if not valid_email(email):
            self.su_error_msg += 'Invalid email: %s' % email
            self.su_missing_fields.append('email1')
            return
        results = self.users.getUsers({'email': email})
        if results:
            self.su_error_msg += 'Email %s already in use, try ' \
                'forgot password.' % email
            return
        # passwords match?
        if self.form['password1'].value != self.form['password2'].value:
            self.su_error_msg += 'Passwords do not match.'
            return

        # user registration
        user_data = {'first_name': self.form['first_name'].value,
                     'last_name' : self.form['last_name'].value,
                     'email'     : self.form['email1'].value,
                     'password'  : self.form['password1'].value,
                     'status_id' : USER_STATUS_PENDING}
        user_school_data= {'school_name'       : self.form['school1'].value,
                           'school_relationship_id':
                               self.form['school_rel1'].value,
                           'original_grade'    : self.form['grade1'].value}
        try:
            Registration().add(user_data, user_school_data)
        except Exception, e:
            self.su_error_msg = 'Oops, there was a problem - Error Code 100'
            return

        # registration complete
        self._clearSUFields()
        self.su_error_msg = 'Registration Complete - you can now login'

    def _clearSUFields(self):
        for field in SIGNUP_FIELDS + SCHOOL_FIELDS:
            self.form[field].value = ''

    def _schoolRelField(self, n, required=0):
        options = {0: ''}
        for id, record in SchoolRelationships().table.items():
            options[id] = record['description']

        name = 'school_rel%s' % n
        cur_value = getattr(self, name)
        return mkDropDownMenu(name, options, cur_value, required=required)

    def _schoolField(self, n, required=0):
        name = 'school%s' % n
        value = getattr(self, name)

        attrs = {} if required else {'disabled': 1}
        attrs['class_'] = 'typeahead'
        return div(input30(name=name, value=value, placeholder='School Name',
                           **attrs),
                   id='school')

    def _gradeField(self, n, required=0):
        options = {0: ''}
        for id, record in Grades().table.items():
            options[id] = record['name']

        name = 'grade%s' % n
        cur_value = getattr(self, name)
        return mkDropDownMenu(name, options, cur_value, required=required)

def mkDropDownMenu(name, options, cur_value, required=0):
    attrs = {'class_': 'selectpicker'}
    if not required:
        attrs['disabled'] = 1

    # sort ids, but put 0 on top
    ids = sorted(options.keys())
    p = ids.index(0)
    ids = [0] + ids[0:p] + ids[p+1:]

    # build select
    options_html = ''
    for id in ids:
        desc = options[id]
        attrs2 = {'selected': 'selected'} if str(id) == cur_value else {}
        options_html += option(desc, value=id, **attrs2) + '\n'

    menu = select(options_html, name=name, **attrs)
    ind = '*' if required else ''

    return nobr(menu + ind)


def input30 (**attrs):
    attrs['size'] = 30
    return htmlSingleTag ('input', attrs)


if __name__ == '__main__':
    Login().go()
