#!/usr/bin/env python

import sys
import os
import time

from vweb.html import *
from vweb.htmltable import HtmlTable

from base import Base
from session import Session

class LoginTest(Base):

   def __init__(self):
      Base.__init__(self, 'Login Test')
      self.debug_cgi = 1
      self.require_login = False

   def process(self):
      Base.process(self)
      self.debug_cgi = True

   def getHtmlContent(self):
      return \
          self._getSessionInfo() + \
          self._getLoginForm()
          #self._getControls()

   def _getSessionInfo(self):
      '''Return Session Info'''

      msg = h3('session info')

      if self.session.new_session:
         msg += p('New Session')

      msg += p('Last Visit: %s' % self.session.last_visit)

      if self.session.logged_in:
         msg += p(self.session.user.email + ' Logged In') + \
             self._getLogoutButton()
      else:
         msg += p('Not Logged in')
      return div(msg, style="margin: 30px")

   def _getLoginForm(self):

      email        = input(name='email', type='text')
      password     = input(name='password', type='password')
      login_button = input(name='login_submit', type='submit',
                           value='Login')
      table = HtmlTable()
      table.addRow(['Email', email])
      table.addRow(['Password', password])
      table.addRow(['', login_button])
      return div(
         table.getTable(),
         style="margin: 30px")

   def _getLogoutButton(self):
      logout = input(name='logout', type='submit', value='Logout')
      return logout


if __name__ == '__main__':
   LoginTest().go()
