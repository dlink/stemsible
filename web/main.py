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
        left = self._getSchoolPanel()
        if self.search:
            center = self.feed.getMessages(search=self.search)
        else:
            center = self.feed.getNewMessageCard() + self.feed.getMessages()

        right = self._getTagsPanel()

        return open('body-section.html', 'r').read() % (left, center, right)

        # 8/25/2016 - removed this form because there are inner forms
        # and you cannot nest forms.  This was causing liking to toggle
        # when user hit like, then posted a test.
        # leaving commented out for a time to see if there are any
        # unexpected results.
        #return form(o, name='form1', method='POST')

    def _getSchoolPanel(self):
        def mk_link(name):
            name2 = name.replace("'", "\\\'")
            return p(name, onclick="javascript:search('%s')" % name2)

        school_header = p('Schools', id='school-header')

        schools = set([s['school'] for s in self.session.user.schools])
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

        tags = ['Music', 'SAT', 'Devices', 'SpecialEd', 'Football', 'Math', 'Research',
                'HonorsClass', 'AP', 'Art', 'LifeSkills', 'DIY', 'CubScouts', 'Health'
                'AfterSchool', 'Meals','Transportation', 'Soccer', 'OpenHouse',
                'SocialMedia', 'Olympics', 'Health', 'Programming', 'Volunteer',
                'Supplies', 'Futura', 'Bullying', 'BackToSchool', 'Beach', 'Basketball',
                'Kindergarten', 'PTA', 'Library', 'Autism', 'FieldTrip',
                'Science', 'Spectrum', 'AOS','Safety',  'CommonCore', 'Grit',
                'Economics', 'ESL', 'Cafeteria', 'AP Latin', 'IB',
                'ACT', 'Movies', 'Technology', 'Parks', 'History', 'Geography',
                'Engineering', 'Economics', 'Literature', 'Geography', 'Drama',
                'Swimming', 'Lacrosse',  'Softball', 'Drones', 'Halloween',
                'Camping', 'Internship', 'Weather', 'Culture', 'Projects', 'Space',
                'SnowDays' ]
        real_tags = ['Music', 'CubScouts', 'Devices', 'SpecialEd', 'Basketball', 'Math',
                     'HonorsClass', 'AP', 'AfterSchool', 'Transportation', 'OpenHouse',
                     'BackToSchool', 'SocialMedia', 'Autism', 'Olympics', 'Health',
                     'Programming', 'FieldTrip', 'Volunteer', 'Soccer', 'Supplies',
                     'Futura', 'Health', 'Bullying', 'Kindergarten', 'PTA', 'Library',
                     'Science', 'Spectrum', 'AOS', 'Safety', 'Beach', 'CommonCore',
                     'Research', 'Football', 'Meals', 'Art', 'LifeSkills', 'DIY', 'Grit',
                     'SAT']

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
