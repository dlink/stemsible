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
        table.addHeader(['Trending Tags'])
        table.addRow([tag_buttons])
        return table.getTable()

def tag_button(tag):
    return input(value=tag, type='button',
                 class_='btn btn-default btn-xs disabled')

if __name__ == '__main__':
    Main().go()
