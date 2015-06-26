#!/usr/bin/env python

from vlib.odict import odict

from vweb.html import *
from vweb.htmlpage import HtmlPage

from messages import Messages

class Main(HtmlPage):

    def __init__(self):
        HtmlPage.__init__(self, 'Stemsible')
        self.style_sheets = ['bootstrap/css/bootstrap.min.css',
                             'css/app.css']
        self.messages = Messages()

    def process(self):
        self.user = odict({'name': 'dlink',
                           'id': 10})

    def getHtmlContent(self):
        return \
            self._getHeader() + \
            self._getBody() + \
            self._getFooter()

    def _getHeader(self):
        return open('header-section.html', 'r').read()

    def _getBody(self):
        return open('body-section.html', 'r').read() % self._getMessages()

    def _getMessages(self):
        messages = self.messages.getMessages()['messages']
        o = ''
        for m in messages:
            o += self._getMessageCard(m)
        return div(o, id='messageArea')

    def _getMessageCard(self, message):
        message = odict(message)
        user_icon = div(img(src='images/generic_icon.png'),
                        class_='img-thumbnail')
        username = div(message.author,  class_='messageAuthor')
        date     = div(message.created, class_='messageDate')
        username_and_date = div(username + date,
                                class_='usernameAndDate')
        buttons = 'Like | Comment'

        o = ''
        o += div(user_icon + username_and_date)
        o += div(message.text, class_='messageText')
        #o += hr()
        #o += div(buttons, class_='messageButtons')

        return div(o, class_='messageCard')

    def _getFooter(self):
        items = ['FAQ', 'About', 'Terms & Privacy', 'Contact']
        #links = [a(i, href='/%s' % i) for i in items]
        o = hr()
        for i in items:
            #o += a(i, href='/%s' % i)
            o += span(i, class_='footerLink')
        return div(o, id='footer')

if __name__ == '__main__':
    Main().go()
