#!/usr/bin/env python

from vlib.odict import odict

from vweb.html import *
from vweb.htmlpage import HtmlPage

from messages import Messages

class Main(HtmlPage):

    def __init__(self):
        HtmlPage.__init__(self, 'Stemsible')
        self.style_sheets = ['css/main.css']
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
        # logo/name
        name = span('Stemsible', id='headerName')

        # search bar
        field = input(name='search', type='textfield',
                      value='Search for activities, answers, and advice',
                      id='searchField')
        search = span(field, id='searchArea')

        # login Info
        href='/user/%s' % self.user.id
        link = a(self.user.name, href=href)
        login_info = span('Logged In as: %s' % link, id='loginInfo')

        return div(
            name +
            search +
            login_info, id='header')

    def _getBody(self):
        messages = self.messages.getMessages()['messages']
        o = ''
        for m in messages:
            o += self._getMessageCard(m)
        o = div(o, id='messageArea')

        return div(o, id='body')

    def _getMessageCard(self, message):
        message = odict(message)

        user_icon = div(img(src='images/generic_icon.png'),
                        class_='userIcon')

        username = div(message.author, class_='messageAuthor')
        date     = div(message.created      , class_='messageDate')
        username_and_date = div(username + date,
                                class_='usernameAndDate')

        buttons = 'Like | Comment'

        o = ''
        o += div(user_icon + username_and_date)
        o += div(message.text, class_='messageText')
        o += hr()
        o += div(buttons, class_='messageButtons')

        return div(o, id='messageCard')

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
