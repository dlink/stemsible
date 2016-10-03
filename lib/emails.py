from passlib.hash import sha256_crypt

import sys

import requests
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadData
from passlib.utils import generate_password

from vlib import conf
from vlib import db
from vlib import logger
from vlib.utils import lazyproperty

USER_STATUS_ACTIVE = 10
forgot_password_text = """
Hello,

Your new password is: {}

Thanks,
Stemsible Team
"""

class EmailError(Exception): pass

class Emails(object):

    SECRET = 'qLXFKsdYv8ycjRAd'
    EXPIRATION = 3600 * 4
    
    @lazyproperty
    def users(self):
        from users import Users
        return Users()
    
    @lazyproperty
    def logger(self):
        return logger.getLogger('Emails')

    def __init__(self):
        self.db = db.getInstance()
        self.config = conf.getInstance()
        self.serializer = Serializer(self.SECRET, expires_in=self.EXPIRATION)

    def send_email(self, to, subject, body, html=None):
        try:
            ret = requests.post(
                "https://api.mailgun.net/v3/stemsible.com/messages",
                auth=("api", self.config.emails.apikey),
                data={"from": "%s <%s>"  % (self.config.emails.name,
                                            self.config.emails.username),
                      "to": to,
                      "subject": subject,
                      "text": body,
                      "html": html})
            self.logger.info('Email sent: %s, %s: %s' % (to, subject, ret))
            return ret
        except Exception, e:
            self.logger.error('Email error: %s, %s' % (to, subject))

    def send_verification_email(self, email):
        user = self.users.getUsers({'email': email})
        if not user:
            self.logger.error('Send_vrification_email: %s not found' % email)
            raise Exception('user not found')
        user = user[0]
        token = self.serializer.dumps(email)
        url = 'http://{}/verify.py?t={}'.format(self.config.baseurl, token)
        path = '%s/lib/emails' % self.config.basedir
        body = open('%s/verification.txt' % path).read() % url
        html = open('%s/verification.html' % path).read() % (url, url)
        self.send_email(email, 'Please verify your email', body, html=html)

    def verify_email_token(self, token):
        try:
            email = self.serializer.loads(token)
            user = self.users.getUsers('email = "%s"' % email)[0]
            user.update('status_id', USER_STATUS_ACTIVE)
            
            #user = Users()
            #user.setFilters('email = "%s"' % email)
            #user.updateRows({'status_id': USER_STATUS_ACTIVE})
            
            self.logger.info('User is verified: {}'.format(email))
            return user
        except BadData:
            return False

    def send_new_password(self, email):
        user = self.users.getUsers({'email': email})
        if not user:
            raise EmailError('Email %s not on file' % email)
        password = generate_password(size=10)
        user = user[0]
        self.db.startTransaction()
        try:
            encrypt_password = sha256_crypt.encrypt(password)
            user = self.users.update({'password': encrypt_password}, email)
            self.db.commit()
        except Exception, e:
            emsg = \
                'Unable to change user password: ' \
                'Error: %s' \
                % (e)
            self.logger.error(emsg)
            self.db.rollback()
            raise
        self.send_email(email,'Your stemsible password',
                        forgot_password_text.format(password))

    def send_welcome_email(self, user):
        path = '%s/lib/emails' % self.config.basedir
        
        body = open('%s/welcome.txt' % path).read() % user.first_name
        html = open('%s/welcome.html' % path).read() % user.first_name
        return self.send_email(user.email, 'Welcome to Stemsible!', body, html=html)

def test_email(to):
    body = 'Hello,\nThis is a test email from Stemsible.\nHave a nice day'
    html = '<h1>Hello</h1><p>This is a test email from stemsible.</p><p>Have a nice day</p>'
    #html = None
    return Emails().send_email(to, 'Test Email', body, html)

if __name__ == '__main__':
    #print Emails().send_verification_email(sys.argv[1])
    #print Emails().verify_email_token(sys.argv[1])
    #print Emails().send_email(sys.argv[1], 'test1', 'test body')
    #print Emails().send_new_password(sys.argv[1])
    #print Emails().send_email(sys.argv[1], 'test1', 'test body', html='<h3>test body</h3>')
    #from users import User
    #print Emails().send_welcome_email(User(sys.argv[1]))
    print test_email(sys.argv[1])
