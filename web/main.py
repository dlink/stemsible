#!/usr/bin/env python

from vlib.odict import odict

from vweb.html import *

from base import Base
from messages import Messages

class Main(Base):

    def __init__(self):
        Base.__init__(self)
        self.messages = Messages()
        self.debug_cgi = 0

    def process(self):
        Base.process(self)

        # add new messages
        if 'new_message' in self.form:
            user_id = self.session.user.id

            data = {'user_id': user_id,
                    'text'   : self.form['new_message'].value}
            id = self.messages.add(data)

    def _getBody(self):
        return open('body-section.html', 'r').read() % (
            self._getSchoolCounty(),
            self._getGroupsPanel(),
            self._getNewMessageCard() +
            self._getMessages(),
            self._getTagsPanel())

    def _getMessages(self):
        user_id = self.session.user.id
        messages = self.messages.getUserMessages(user_id)['messages']
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
        reason   = div(message.reason)
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


    def _getSchoolCounty(self):
        items = ['Creightons Corner Elementary', 'Loudoun County Public Schools']
        schoolcounty = ''
        for i in items:
            schoolcounty += '<tr><td><li>' + i + '</li></td></tr>'
        return schoolcounty

    def _getGroupsPanel(self):
        items = ['CCE PTA', 'CCE Garden Committee', 'LCPS Math Olympiad']
        groups = ''
        for i in items:
            groups += '<tr><td><li>' + i + '</li></td></tr>'
        return groups

    def _getTagsPanel(self):
        items = ['SAT', 'Snow Days', 'Special Needs', 'Basketball', 'Economics']
        tags = ''
        for i in items:
            tags += '<button type="button" class="btn btn-default btn-sm">' + i + '</button>'
        return tags

if __name__ == '__main__':
    Main().go()
