#!/usr/bin/env python

from vlib.odict import odict

from vweb.html import *
from vweb.htmltable import HtmlTable

from base import Base
from messages import Messages, Message
from messagelikes import MessageLikes, addHeaders as messageLikes_addHeaders
from messagecomments import MessageComments, \
    addHeaders as messageComments_addHeaders

class Main(Base):

    def __init__(self):
        Base.__init__(self)
        messageLikes_addHeaders(self)
        messageComments_addHeaders(self)

        self.messages = Messages()
        self.scroll_pos = 0
        self.debug_cgi = 0

    def process(self):
        Base.process(self)

        # add new messages
        if 'new_message' in self.form:
            data = {'user_id': self.session.user.id,
                    'text'   : self.form['new_message'].value}
            id = self.messages.add(data)

        # add like
        if 'like' in self.form:
            message_id = int(self.form['like'].value)
            if message_id:
                message = Message(message_id)
                MessageLikes(message).toggle(self.session.user.id)

        # add comment
        for field in self.form.keys():
            if field.startswith('new_comment_'):
                reference_id = field.split('_')[2]
                if reference_id:
                    data = {'user_id': self.session.user.id,
                            'reference_id': reference_id,
                            'text': self.form[field].value}
                    id = self.messages.add(data)
                break;

        # remember scroll
        if 'scroll_pos' in self.form:
            self.scroll_pos =int(round(float(self.form['scroll_pos'].value),0))

    def _getBody(self):
        left   = self._getSchoolPanel()
        center = self._getNewMessageCard() + self._getMessages()
        right  = self._getTagsPanel()

        # hack
        bot = '<script>$(document).scrollTop(%s);</script>' % self.scroll_pos

        return open('body-section.html', 'r').read() \
            % (left, center, right) + bot

    def _getMessages(self):
        user_id = self.session.user.id
        messages = self.messages.getUserMessages(user_id)['messages']

        hidden_fields = \
            input(name='like', type='hidden') + \
            input(name='scroll_pos', type='hidden')

        o = ''
        o += hidden_fields
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

        messageLikes = MessageLikes(message)
        messageComments = MessageComments(message)

        # TO DO: Change this mess into:
        #    messageComments.html_widge(self.user)
        if message.id == 71:
            num_comments = 3
        else:
            num_comments = 0
        comment = span(img(src='images/comment.png') + str(num_comments),
                       title='Comment on this',
                       class_='messageFooterButton')

        footer = \
            messageLikes.html_widget(self.session.user) + \
            messageComments.html_widget()

        o = ''
        o += user_icon + username_and_date
        o += div(message.text, class_='messageText')
        o += div(footer, class_='messageFooter')
        o += messageLikes.html_likersSection()
        o += messageComments.html_commentsSection(self.session.user)

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
            return input(value=tag, type='button',
                         class_='btn btn-default btn-xs disabled')

        tags = ['SAT', 'Snow Days', 'Special Needs', 'Basketball', 'Economics',
                'Cafeteria', 'ESL', 'AP Latin', 'Programming', 'Movies',
                'Field Trips']
        tag_buttons = ''.join([mkbutton(t) for t in tags])

        table = HtmlTable(class_='table borderless')
        table.addHeader(['Trending Tags'])
        table.addRow([tag_buttons])
        return table.getTable()

def tag_button(tag):
    return input(value=tag, type='button',
                 class_='btn btn-default btn-xs disabled')

if __name__ == '__main__':
    Main().go()
