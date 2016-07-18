#!/usr/bin/env python

from vlib.utils import format_date, valid_email, lazyproperty
from vlib import logger
from vweb.html import *
from vweb.htmltable import HtmlTable

from base import Base
from grades import Grades
from registration import Registration
from schoolrelationships import SchoolRelationships
from schoolinfo import SchoolInfo
from emails import Emails

USER_STATUS_PENDING = 8

LOGIN_FIELDS = ['email', 'password']
SIGNUP_FIELDS = ['email1', 'first_name', 'last_name', 'password1','password2']
SCHOOL_FIELDS = ['school_rel', 'school', 'grade']

class Login(Base):

    @lazyproperty
    def logger(self):
        return logger.getLogger('Login')

    def __init__(self):
        Base.__init__(self)
        self.schoolInfo = SchoolInfo()
        self.emails = Emails()

        self.style_sheets.extend(['css/home.css', 'css/signup.css'])
        self.javascript_src.extend(['js/signup.js'])
        self.javascript_src.extend(self.schoolInfo.getJsFile())

        self.require_login = False
        self.error_msg = ''
        self.su_user_msg = []
        self.missing_fields = []

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
            value = self.form[f].value if (f in self.form) else ''
            setattr(self, f, value)

            # init values in schoolInfo object
            if f == 'school':
                self.schoolInfo.school = value
            elif f in ('school_rel', 'school', 'grade'):
                setattr(self.schoolInfo, f, value or 0)

    def _processSignUp(self):
        # check required fields:
        for field in SIGNUP_FIELDS + ['school']:
            if field not in self.form or not self.form[field].value:
                self.missing_fields.append(field)

        # chech required drop down menus
        for field in ['school_rel', 'grade']:
            if field not in self.form or not int(self.form[field].value):
                self.missing_fields.append(field)

        # sign up error message
        if self.missing_fields:
            self.error_msg += 'Please fill in required fields marked in red'
            self.schoolInfo.missing_values = self.missing_fields
            return

        # email cool?
        email = self.form['email1'].value
        if not valid_email(email):
            self.error_msg += 'Invalid email: %s' % email
            self.missing_fields.append('email1')
            return

        # email already in use?
        results = self.users.getUsers({'email': email})
        if results:
            self.error_msg += 'Email %s already in use, try ' \
                'forgot password.' % email
            self.missing_fields.append('email1')
            return

        # passwords match?
        if self.form['password1'].value != self.form['password2'].value:
            self.error_msg += 'Passwords do not match.'
            self.missing_fields.append('password1')
            self.missing_fields.append('password2')
            return

        # user registration
        user_data = {'first_name': self.form['first_name'].value,
                     'last_name' : self.form['last_name'].value,
                     'email'     : self.form['email1'].value,
                     'password'  : self.form['password1'].value,
                     'status_id' : USER_STATUS_PENDING}
        user_school_data= {'school_name'   : self.form['school'].value,
                           'school_relationship_id':
                               self.form['school_rel'].value,
                           'original_grade': self.form['grade'].value}
        try:
            Registration().add(user_data, user_school_data)
        except Exception, e:
            self.error_msg = 'Oops, there was a problem - Error Code 100'
            return

        try:
            self.emails.send_verification_email(email)
        except Exception, e:
            self.error_msg = 'Opps, unable to send confirmation email - ' \
                             'Error Code 200'
            self.logger.error('Unable to send_verification_email(%s): %s' \
                              % (email, e))
            return

        # email verification sent
        self._clearFields()
        self.su_user_msg = 'Great! An email was sent to %s.  Please ' \
                           'open it and click on the link it contains ' \
                           'to complete registraion.' % email

    def _getBody(self):
        return open('home.html', 'r').read() % self._getSignUpNow()

    def _getSignUpNow(self):

        attr = lambda f: {'class_':'red'} \
            if f in self.missing_fields else {}

        # Header

        head1 = h2('Sign Up Now', id='head1')
        head2 = h2(small("It's free and it always will be"),id='head2')

        # User msg

        su_user_msg =  self._getSUUserMsg()

        # Basic Info

        o = ''
        fields = ['email1', 'first_name', 'last_name', 'password1',
                  'password2']
        for f in fields:
            o += self._getSignUpField(f, attr)


        # School Info

        o += div(''.join(self.schoolInfo.schoolFields()), class_='form-group')

        # Sign Up Button

        signup = input(name='signup', class_='form-control btn btn-info',
                       type='submit', value='Sign Up')
        o += div(signup, class_='form-group')


        return head1 + head2 + su_user_msg + form(o, name='signup-form',
                                                  method='POST')

    def _getSignUpField(self, name, attr):
        '''Given a field name (in lowercase)
           return HTML String of
              label and input field in a form group

              Email* [                ]
        '''

        type  = 'text'
        lname = name.title().replace('_', ' ')
        extra = ''

        if name == 'email1':
            type = 'email'
            lname = 'Email'
        elif name == 'password1':
            type = 'password'
            lname = 'Password'
            extra = span('', id='passstrength')
        elif name == 'password2':
            type = 'password'
            lname = 'Confirm Password'
            extra = span('', id='passmatch')

        #flabel = label(lname + '*',
        #               for_=name+'-input',
        #               **attr(name))

        class_ = 'form-control'
        if name in self.missing_fields:
            class_ += ' missing-value'

        field = input(type=type,
                      name=name,
                      class_=class_,
                      id=name+'-input',
                      placeholder=lname,
                      value=getattr(self, name))


        return div(field + extra, class_='form-group')

    def _getSUUserMsg(self):
        o = ''
        if self.su_user_msg:
            o += p(self.su_user_msg, class_='user-message')
        if self.error_msg:
            o += p(self.error_msg, class_='error-message')
        return o

    def _clearFields(self):
        for field in SIGNUP_FIELDS + SCHOOL_FIELDS:
            self.form[field].value = ''

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

if __name__ == '__main__':
    Login().go()
