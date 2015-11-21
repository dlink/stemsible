#!/usr/bin/env python

from vlib.odict import odict

from vweb.html import *
from vweb.htmltable import HtmlTable

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
        left   = self._getSchoolPanel()
        center = self._getNewMessageCard() + self._getMessages()
        right  = self._getTagsPanel()

        return open('body-section.html', 'r').read() % (left, center, right)

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

    def _getSchoolPanel(self):
        schools = ['Creightons Corner Elementary',
                   'Loudoun County Public Schools']
        table = HtmlTable(class_='table borderless truncate')
        table.addHeader(['School & County'])
        for school in schools:
            table.addRow([li(school)])

        groups = ['CCE PTA', 'CCE Garden Committee', 'LCPS Math Olympiad']
        table2 = HtmlTable(class_='table borderless truncate')
        table2.addHeader(['Groups'])
        for group in groups:
            table2.addRow([li(group)])
        return div(p('') + table.getTable() + table2.getTable(),
                   id='school-panel')

    def _getTagsPanel(self):
        def mkbutton(tag):
            return input(
                value=tag, type='button', class_='btn btn-default btn-xs disabled')

        tags = ['SAT', 'Snow Days', 'Special Needs', 'Basketball', 'Economics',
                 'Cafeteria', 'ESL', 'AP Latin', 'Programming', 'Movies', 'Field Trips']
        tag_buttons = ''.join([mkbutton(t) for t in tags])

        table = HtmlTable(class_='table borderless')
        table.addHeader(['Trending Tags'])
        table.addRow([tag_buttons])
        return table.getTable()

def tag_button(tag):
    return input(value=tag, type='button', class_='btn btn-default btn-xs disabled')


if __name__ == '__main__':
    Main().go()
