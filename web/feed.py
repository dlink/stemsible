#!/usr/bin/env python

import re

from vlib import conf
from vlib.odict import odict

from vweb.html import *
from vweb.htmltable import HtmlTable

from encryptint import encrypt_int, decrypt_int

from messages import Messages, Message
from messagelikes import MessageLikes, addHeaders as messageLikes_addHeaders
from messagecomments import MessageComments, \
    addHeaders as messageComments_addHeaders

from images import getUserImage


class Feed(object):

    def __init__(self, page):
        self.page = page
        self.conf = conf.getInstance()
        messageLikes_addHeaders(page)
        messageComments_addHeaders(page)

        self.messages = Messages()
        self.scroll_pos = 0
        self.num_messages = None

    def process(self):

        # add new messages
        if 'new_message' in self.page.form:
            data = {'user_id': self.page.session.user.id,
                    'text': self.page.form['new_message'].value}
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
                break

        # remember scroll
        if 'scroll_pos' in self.page.form:
            p = self.page.form['scroll_pos'].value
            self.scroll_pos = int(round(float(p), 0))

    def getMessages(self, user_id=None, search=None):
        # TO DO: rename getMyMessages to something like getThisUsersMessages

        if search:
            messages = self.messages.getSearchMessages(search)['messages']
        else:
            if not user_id:
                user_id = self.page.session.user.id
            if self.page.name == 'profile':
                messages = self.messages.getMyMessages(user_id)['messages']
            else:
                messages = self.messages.getUserMessages(user_id)['messages']

        self.num_messages = len(messages)

        hidden_fields = \
            input(name='like', type='hidden') + \
            input(name='scroll_pos', type='hidden') + \
            input(name='prev_scroll_pos', type='hidden', value=self.scroll_pos)

        o = ''
        o += hidden_fields
        for m in messages:
            o += self._getMessageCard(m, search=search)
        return form(div(o, id='messageArea'), name='messages-form')

    def getNewMessageCard(self):
        return form(open('new-message2.html', 'r').read(),
                    name='new-card-form')

    def _getMessageCard(self, message, search=None):
        message = odict(message)
        image = getUserImage(message.user_id)
        user_icon = div(img(src=image, width='70px',
                            class_='img-thumbnail'),
                        class_='userIcon')
        username = div(message.author,  class_='messageAuthor')
        reason = div(message.reason, class_='messageReason')
        date = div(message.created, class_='messageDate')
        name_link = a(username, href='//%s/profile.py?u=%s'
                      % (self.conf.baseurl, encrypt_int(message.user_id)))
        username_and_date = div(name_link + reason + date,
                                class_='usernameAndDate')

        text = self._highlightKeyTerms(message.text, search)

        messageLikes = MessageLikes(message)
        messageComments = MessageComments(message)
        footer = \
            messageLikes.html_widget(self.page.session.user) + \
            messageComments.html_widget()

        o = ''
        o += user_icon + username_and_date
        o += div(text, class_='messageText')
        o += div(footer, class_='messageFooter')
        o += messageLikes.html_likersSection()
        o += messageComments.html_commentsSection(self.page.session.user,
                                                  search=search)

        return div(o, class_='messageCard', id='message_card_%s' % message.id)

    def _highlightKeyTerms(self, text, search=None):
        if not search:
            return text

        text2 = text
        for term in search.split(' '):
            term2 = r'(%s)' % term
            text2 = re.sub(term2, r'<span class="search-term">\1</span>',
                           text2, flags=re.IGNORECASE)
        return text2
