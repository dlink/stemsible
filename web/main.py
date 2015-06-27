#!/usr/bin/env python

import os

from vlib.odict import odict

from vweb.html import *
from vweb.htmlpage import HtmlPage

from users import Users
from messages import Messages

class Main(HtmlPage):

    def __init__(self):
        HtmlPage.__init__(self, 'Stemsible') #, include_form_tag=0)
        self.style_sheets = ['bootstrap/css/bootstrap.min.css',
                             'css/app.css']
        self.users = Users()
        self.messages = Messages()
        self.debug_cgi = 0

    def process(self):
        HtmlPage.process(self)

        # get user
        username = os.environ['REMOTE_USER']
        self.user = self.users.getUsers({'username': username})[0]

        # add new messages
        if 'new_message' in self.form:
            data = {'user_id': self.user.id,
                    'text'   : self.form['new_message'].value}
            id = self.messages.add(data)

    def getHtmlContent(self):
        return \
            self._getHeader() + \
            self._getBody() + \
            self._getFooter()

    def _getHeader(self):
        return open('header-section.html', 'r').read()

    def _getBody(self):
        return open('body-section.html', 'r').read() % (
            self._getNewMessageCard() +
            self._getMessages())

    def _getMessages(self):
        messages = self.messages.getMessages()['messages']
        o = ''
        for m in messages:
            o += self._getMessageCard(m)
        return div(o, id='messageArea')

    def _getNewMessageCard(self):
        return open('new-message2.html', 'r').read()

    def _getMessageCard(self, message):
        message = odict(message)
        user_icon = div(img(src='images/generic_icon.png',
                            class_='img-thumbnail'),
                        class_='userIcon')
        username = div(message.author,  class_='messageAuthor')
        date     = div(message.created, class_='messageDate')
        username_and_date = div(username + date,
                                class_='usernameAndDate')
        buttons = 'Like | Comment'

        o = ''
        o += user_icon + username_and_date
        o += div(message.text, class_='messageText')
        #o += hr()
        #o += div(buttons, class_='messageButtons')

        return div(o, class_='messageCard', id='message_card_%s' % message.id)

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

if __name__ == '__main__':
    Main().go()
