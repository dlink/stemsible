#!/usr/bin/env python

import sys
import os
import time
from session import Session

from vweb.html import *
from vweb.htmltable import HtmlTable

from base import Base

class SessionTest(Base):

   def process(self):
      Base.process(self)
      self.debug_cgi = True
      

   def getHtmlContent(self):
      return \
          self._getSessionInfo() + \
          self._getControls()

   def _getSessionInfo(self):
      '''Return Session Info'''

      msg = h3('session info')

      if self.session.new_session:
         msg += p('New Session')

      msg += p('Last Visit: %s' % self.session.last_visit)

      if self.session.logged_in:
         msg += p('Logged In')
      else:
         msg += p('Not Logged in')
      return div(msg, style="margin: 30px")

   def _getControls(self):
      login_as_dlink = input(name='login', type='submit',
                             value='Login as dlink')
      logout = input(name='logout', type='submit', value='Logout')

      table = HtmlTable()
      table.addRow([login_as_dlink, logout])
      return div(
         table.getTable(),
         style="margin: 30px")

if __name__ == '__main__':
   SessionTest().go()
