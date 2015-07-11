#!/usr/bin/env python

import os

from vlib.odict import odict

from vweb.html import *
from vweb.htmlpage import HtmlPage

from users import Users
from messages import Messages

USER_CHOOSER = 1

class Main(HtmlPage):

    def __init__(self):
        HtmlPage.__init__(self, 'Stemsible') #, include_form_tag=0)
        self.style_sheets = ['bootstrap/css/bootstrap.min.css',
                             'css/app.css']
        if USER_CHOOSER:
            self.style_sheets.append('css/userchooser.css')
        self.users = Users()
        self.messages = Messages()
        self.debug_cgi = 0

    def process(self):
        HtmlPage.process(self)

        # get user
        username = os.environ['REMOTE_USER']
        self.user = self.users.getUsers({'username': username})[0]

       # substitute user
        self.su_user = self.user.id
        if 'user_chooser' in self.form:
            self.su_user = int(self.form['user_chooser'].value)
        #self.debug_msg += p('substitute user: %s' % self.su_user)

        # add new messages
        if 'new_message' in self.form:
            if USER_CHOOSER:
                user_id = self.su_user
            else:
                user_id = self.user.id

            data = {'user_id': user_id,
                    'text'   : self.form['new_message'].value}
            id = self.messages.add(data)

    def getHtmlContent(self):
        return \
            self._getHeader() + \
            self._getBody() + \
            self._getFooter()

    def _getHeader(self):
        return open('header-section2.html', 'r').read() % \
            (self.user.fullname,
             self._getUserChooser())

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

    def _getUserChooser(self):
        '''Used for debug
           provide a drop down of different users
        '''
        if not USER_CHOOSER:
            return ''

        options = ''
        #keys = ['select a substitute user', 'Sally', 'George', 'Ringo', 'Felip']
        #for key in keys:
        #    if key == self.su_user:
        #        options += option(key, value=key, selected='1')
        #    else:
        #        options += option(key, value=key)
        #return select(options, name='user_chooser', id='user_chooser',
        #              onChange='submit()', class_='selectpicker')

        for id, username in self.users.getUserMap():
            if id == self.su_user:
                options += option(username, value=id, selected='1')
            else:
                options += option(username, value=id)
        return select(options, name='user_chooser', id='user_chooser',
                      onChange='submit()', class_='selectpicker')


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
