import sys
from vlib import conf
from vlib import db
from vlib import logger
from vlib.utils import lazyproperty
from sender import Mail, Message, SenderError
from users import Users
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadData

USER_STATUS_ACTIVE = 10

class Emails(object):

    SECRET = 'qLXFKsdYv8ycjRAd'
    EXPIRATION = 3600 * 4

    @lazyproperty
    def logger(self):
        return logger.getLogger('Emails')

    def __init__(self):
        self.db = db.getInstance()
        self.config = conf.getInstance()
        self.serializer = Serializer(self.SECRET, expires_in=self.EXPIRATION)
        self.gmail = Mail('smtp.gmail.com', port=587, use_tls=True,
                          username=self.config.emails.username,
                          password=self.config.emails.password)

    def send_email(self, to, subject, body, html=None):
        message = Message(subject=subject, body=body, html=html,
                          to=to, fromaddr=(self.config.emails.name,
                                           self.config.emails.username))
        try:
            self.gmail.send(message)
        except SenderError as e:
            self.logger.error('Email send error: {}'.format(e))
        else:
            self.logger.info('Email sent to: {}'.format(to))

    def send_verification_email(self, email):
        user = Users().getUsers({'email': email})
        if not user:
            raise Exception('user not found')
        user = user[0]
        token = self.serializer.dumps(email)
        url = 'http://{}/verify.py?t={}'.format(self.config.baseurl, token)
        path = '%s/lib/emails' % self.config.basedir
        body = open('%s/verification.txt' % path).read() % url
        html = open('%s/verification.html' % path).read() % url
        self.send_email(email, 'Please verify your email', body, html=html)

    def verify_email_token(self, token):
        try:
            email = self.serializer.loads(token)
            user = Users()
            user.setFilters('email = "%s"' % email)
            user.updateRows({'status_id': USER_STATUS_ACTIVE})
            self.logger.info('User is verified: {}'.format(email))
            return True
        except BadData:
            return False


if __name__ == '__main__':
    #Emails().send_verification_email(sys.argv[1])
    #print Emails().verify_email_token(sys.argv[1])
    print Emails().send_email(sys.argv[1], 'test1', 'test body', html='<h3>test body</h3>')
