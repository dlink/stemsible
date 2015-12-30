#!/usr/bin/env python

from vlib.utils import format_date
from vweb.html import *
from vweb.htmltable import HtmlTable
from vlib.odict import odict

from session import Session
from base import Base
from messages import Messages

class Profile(Base):

    def __init__(self):
        Base.__init__(self)
        self.style_sheets.append('css/profile.css')
        self.debug_cgi = 0
        self.session = Session()
        self.messages = Messages()

    def process(self):
        Base.process(self)

        # add new messages
        if 'new_message' in self.form:
            user_id = self.session.user.id

            data = {'user_id': user_id,
                    'text'   : self.form['new_message'].value}
            id = self.messages.add(data)

    def _getBody(self):
        left = ''
        center = \
            self._getProfileUserHeader() + \
            self._getGeneralInfo()
        right = self._getProfilePostsHeader() + \
                self._getNewMessageCard() + \
                self._getMessages()

        return open('profile-section.html', 'r').read() % (left, center, right)

    def _getProfileUserHeader(self):
        return h3('My Profile')

    def _getGeneralInfo(self):
        table = HtmlTable(class_='profileTable')
        data = [
            ['Name'  , self.session.user.fullname],
            ['Email' , self.session.user.email],
            ['Member Since', format_date(self.session.user.created)],
            ]

        #followers
        for i, f in enumerate(self.session.user.following):
            if i == 0:
                row_header = 'Following'
            else:
                row_header = ''
            data.append([row_header, f.fullname])

        for row in data:
            row_header = span(row[0], class_='profileRowHeader')
            value      = row[1]
            table.addRow([row_header, value])
        return table.getTable()

    def _getProfilePostsHeader(self):
        return h3('My Posts')

    def _getMessages(self):
        user_id = self.session.user.id
        messages = self.messages.getMyMessages(user_id)['messages']
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
        reason   = div(message.reason, class_='messageReason')
        date     = div(message.created, class_='messageDate')
        username_and_date = div(username + reason + date,
                                class_='usernameAndDate')
        buttons = 'Like | Comment'

        o = ''
        o += user_icon + username_and_date
        o += div(message.text, class_='messageText')
        #o += hr()
        #o += div(buttons, class_='messageButtons')

        return div(o, class_='messageCard', id='message_card_%s' % message.id)

if __name__ == '__main__':
    Profile().go()
