#!/usr/bin/env python

from vlib.odict import odict

from vweb.html import *
from vweb.htmltable import HtmlTable

from base import Base
from messages import Messages, Message
from messagelikes import MessageLikes, addHeaders as messageLikes_addHeaders

class Main(Base):

    def __init__(self):
        Base.__init__(self)
        messageLikes_addHeaders(self)

        self.messages = Messages()
        self.scroll_pos = 0
        self.debug_cgi = 0

    def process(self):
        Base.process(self)

        # add new messages
        if 'new_message' in self.form:
            user_id = self.session.user.id

            data = {'user_id': user_id,
                    'text'   : self.form['new_message'].value}
            id = self.messages.add(data)

        # add like
        if 'like' in self.form:
            message_id = int(self.form['like'].value)
            if message_id:
                message = Message(message_id)
                MessageLikes(message).toggle(self.session.user.id)

        # remember scroll
        if 'scroll_pos' in self.form:
            self.scroll_pos = int(round(float(self.form['scroll_pos'].value), 0))

    def _getBody(self):
        left   = self._getSchoolPanel()
        center = self._getNewMessageCard() + self._getMessages()
        right  = self._getTagsPanel()

        # hack
        bot = '<script>$(document).scrollTop(%s);</script>' % self.scroll_pos

        return open('body-section.html', 'r').read() % (left, center, right) + bot

    def _getMessages(self):
        user_id = self.user = self.session.user.id
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

        # TO DO: Change this mess into:
        #    messageComments.html_widge(self.user)
        if message.id == 71:
            num_comments = 3
        else:
            num_comments = 0
        comment = span(img(src='images/comment.png') + str(num_comments),
                       title='Comment on this',
                       class_='messageFooterButton')

        footer = messageLikes.html_widget(self.user) + \
            comment + i('(comments pending)')

        o = ''
        o += user_icon + username_and_date
        o += div(message.text, class_='messageText')
        o += div(footer, class_='messageFooter')
        o += div(self._getLikersSection(messageLikes))
        o += div(self._getComments(message), class_='messageComments')

        return div(o, class_='messageCard', id='message_card_%s' % message.id)

    def _getLikersSection(self, messageLikes):
        desc = p('Liked by:')
        likers = ', '.join([b(n['user_fullname'])
                            for n in messageLikes.likes])
        return div(desc + likers, class_='likers', id='likers_%s'
                   % messageLikes.message.id)


    def _getComments(self, message):
        return ''
        o = ''
        if message.id == 71:
            o += hr()
            o += p(b('David Link') + '11/21 - Yeah, you say that but do you mean it?')
            o += p(b('Uday Kumar') + '11/21 - Of course I mean it!')
            o += p(b('David Link') + '11/21 - These are test comments.  This one is a little bit longer than the others.  Does a person know thyself from the nature of their post comments?')
        return o

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
