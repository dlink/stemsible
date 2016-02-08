#!/usr/bin/env python

from vlib.odict import odict

from vweb.html import *
from vweb.htmltable import HtmlTable

from messages import Messages, Message
from messagelikes import MessageLikes, addHeaders as messageLikes_addHeaders
from messagecomments import MessageComments, \
    addHeaders as messageComments_addHeaders

class Feed(object):

    def __init__(self, page):
        self.page = page
        messageLikes_addHeaders(page)
        messageComments_addHeaders(page)

        self.messages = Messages()
        self.scroll_pos = 0

    def process(self):

        # add new messages
        if 'new_message' in self.page.form:
            data = {'user_id': self.page.session.user.id,
                    'text'   : self.page.form['new_message'].value}
            id = self.messages.add(data)

        # add like
        if 'like' in self.page.form:
            message_id = int(self.page.form['like'].value)
            if message_id:
                message = Message(message_id)
                MessageLikes(message).toggle(self.page.session.user.id)

        # add comment
        for field in self.page.form.keys():
            if field.startswith('new_comment_'):
                reference_id = field.split('_')[2]
                if reference_id:
                    data = {'user_id': self.page.session.user.id,
                            'reference_id': reference_id,
                            'text': self.page.form[field].value}
                    id = self.messages.add(data)
                break;

        # remember scroll
        if 'scroll_pos' in self.page.form:
            p = self.page.form['scroll_pos'].value
            self.scroll_pos = int(round(float(p),0))

    def getMessages(self):
        user_id = self.page.session.user.id
        if self.page.name == 'profile':
            messages = self.messages.getMyMessages(user_id)['messages']
        else:
            messages = self.messages.getUserMessages(user_id)['messages']

        hidden_fields = \
            input(name='like', type='hidden') + \
            input(name='scroll_pos', type='hidden')

        o = ''
        o += hidden_fields
        for m in messages:
            o += self._getMessageCard(m)
        return div(o, id='messageArea')

    def getNewMessageCard(self):
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
        footer = \
            messageLikes.html_widget(self.page.session.user) + \
            messageComments.html_widget()

        o = ''
        o += user_icon + username_and_date
        o += div(message.text, class_='messageText')
        o += div(footer, class_='messageFooter')
        o += messageLikes.html_likersSection()
        o += messageComments.html_commentsSection(self.page.session.user)

        return div(o, class_='messageCard', id='message_card_%s' % message.id)
