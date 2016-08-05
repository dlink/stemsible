#!/usr/bin/env python

# Session Class
# Taken originally from
#   http://webpython.codepoint.net/cgi_session_class

import os
import sha
import shelve
import time
import Cookie
from passlib.hash import sha256_crypt

from vlib import conf
from vlib import logger
from vlib.utils import lazyproperty

from users import User, Users

class SessionError(Exception): pass
class SessionErrorLoginFail(SessionError): pass

class Session(object):
   '''Preside over the User Session'''

   @lazyproperty
   def logger(self):
      return logger.getLogger('Session')

   def __init__(self):
      self.conf = conf.getInstance()
      self.new_session = True
      self._logged_in = False
      self._user = None
      self.last_visit = None

      # get cookie
      string_cookie = os.environ.get('HTTP_COOKIE', '')
      self.cookie = Cookie.SimpleCookie()
      self.cookie.load(string_cookie)
      if self.cookie.get('sid'):
         self.new_session = False
         sid = self.cookie['sid'].value
         self.cookie.clear()
      else:
         self.cookie.clear()
         sid = sha.new(repr(time.time())).hexdigest()

      self.cookie['sid'] = sid
      self.cookie['sid']['path'] = '/'
      self.cookie['sid']['expires'] = 30*24*60*60  # 30 days

      # persist session data
      session_dir = self.conf.sessions.dir
      try:
         self.data = shelve.open(session_dir + '/sess_' + sid, writeback=True)
         os.chmod(session_dir + '/sess_' + sid, 0660)
      except Exception, e:
         raise SessionError('Unable to write session data to %s: %s'
                            % (session_dir, e))

      # check logged in
      if self.data.get('logged_in'):
         self._logged_in = 1
         self._user_id   = self.data.get('user_id')

      # Initializes the expires data
      if not self.data.get('cookie'):
         self.data['cookie'] = {'expires':''}

      # last visit
      self.data['lastvisit'] = last_visit_secs = repr(time.time())
      self.last_visit = time.asctime(time.gmtime(float(last_visit_secs)))

      # expiration
      self.data['cookie']['expires'] = 30*24*60*60 # 30 days

   def login(self, email, password):
      '''Log user in by email and password

         Sets Memory: logged_in, user_id and _user
         Persists   : logged_in, user_id

         Throws:  SessionErrorLoginFail
      '''

      # get user
      self.users = Users()
      results = self.users.getUsers({'email': email, 'status_id': self.users.ACTIVE_STATUS})
      if not results or not sha256_crypt.verify(password, results[0].password):
         self.logger.info('Login Fail: %s' %  email)
         raise SessionErrorLoginFail('Incorrect Email or Password')
      self._user = results[0]

      # update instance vars, and
      # persistent session vars (when session.close() is called)
      self.data['logged_in'] = self._logged_in = 1
      self.data['user_id']   = self._user_id   = self._user.id

      # log
      self.logger.info('Login: %s' %  email)

   def logout(self):
      email = self.user.email
      self.data['logged_in'] = 0
      self._logged_in = 0
      self.logger.info('Logout: %s' % email)

   @property
   def logged_in(self):
      return self._logged_in

   @property
   def user(self):
      '''Return current user object
           User gets instanciated during login process, or
           here if already logged in
      '''
      if not self.logged_in:
         raise SessionError('Not logged in')
      if not self._user:
         self._user = User(self._user_id)
      return self._user

   def close(self):
      self.data.close()

def hash_pass(passwd):
   '''Encrypt passwd'''
   return sha256_crypt.encrypt(passwd)

if __name__ == '__main__':
   # encrypt a password
   import sys
   print hash_pass(sys.argv[1])
