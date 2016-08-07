#!/usr/bin/env python

from vweb.html import *
from vweb.htmltable import HtmlTable

from base import Base
from feed import Feed

class Main(Base):

    @property
    def name(self): return 'main'

    def __init__(self):
        Base.__init__(self)
        self.style_sheets.append('css/feed.css')
        self.javascript_src.extend(['js/tags.js'])

        self.feed = Feed(self)
        self.debug_cgi = 0

    def process(self):
        Base.process(self)
        self.feed.process()

        if 'search' in self.form:
            self.search = self.form['search'].value.strip()

    def _getBody(self):
        left   = self._getSchoolPanel()
        if self.search:
            center = self.feed.getMessages(search=self.search)
        else:
            center = self.feed.getNewMessageCard() + self.feed.getMessages()

        right  = self._getTagsPanel()

        # hack
        #bot = '<script>$(document).scrollTop(%s);</script>' \
        #    % self.feed.scroll_pos
        bot = ''

        o = open('body-section.html', 'r').read() \
            % (left, center, right) + bot
        return form(o, name='form1', method='POST')

    def _getSchoolPanel(self):
        def mk_link(name):
            name2 = name.replace("'", "\\\'")
            return p(name, onclick="javascript:search('%s')" % name2)

        school_header = p('Schools', id='school-header')

        schools = [s['school'] for s in self.session.user.schools]
        links = ''
        for school in schools:
            links += li(mk_link(school), class_='cursor-pointer')
        school_links = ul(links)

        return div(school_header + school_links, id='school-panel')

    def _getTagsPanel(self):
        def mk_button(tag, class_=''):
            return input(value=tag, type='button',
                         class_='btn btn-default btn-xs',
                         onclick="javascript: search('%s')" % tag)
        def mk_mock_button(tag, class_=''):
            class_ += ' btn btn-default btn-xs'
            return input(value=tag, type='button',
                         class_='btn btn-default btn-xs disabled')

        tags = ['Saxophone', 'SAT', 'Snow Days', 'Special Needs', 'Basketball',
                'Economics', 'Cafeteria', 'ESL', 'AP Latin', 'Programming',
                'Movies', 'Field Trips']
        real_tags = ['Saxophone']

        tag_buttons = ''
        for tag in tags:
            if tag in real_tags:
                tag_buttons += mk_button(tag)
            else:
                tag_buttons += mk_mock_button(tag)

        table = HtmlTable(class_='table borderless')
        table.addHeader(['Trending Topics'])
        table.addRow([tag_buttons])
        return table.getTable()

def tag_button(tag, class_=''):
    return input(value=tag, type='button',
                 class_='btn btn-default btn-xs',
                 onclick="javascript: search('%s')" % tag)

if __name__ == '__main__':
    Main().go()
