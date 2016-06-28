#!/usr/bin/env python

import unittest

from urls import Urls

# Fixtures

TEST_URLS = [
    'crowfly.net',
    'dev.crowfly.net',
    'www.loudoun.k12.va.us/page/101110',
    'www.youtube.com/channel/UCeY0bbntWzzVIaj2z3QigXg',
    'www.arborday.org/Trees/treeguide/TreeDetail.cfm?ItemID=861',
    'www.arborday.org/Trees/treeguide/TreeDetail.cfm?ItemID=861&zpid=1&ypid=3',
    'www.instagram.com/p/',

    'http://crowfly.net',
    'http://dev.crowfly.net',
    'http://dev.crowfly.net/',
    'http://dev.crowfly.net/a_file.ext',
    'http://dev.crowfly.net/a_file.ext.ext2',
    'http://dev.crowfly.net/foo',
    'http://dev.crowfly.net/foo/bar',
    'http://dev.crowfly.net/foo/bar/baz',
    'http://dev.crowfly.net/foo/bar/baz/a_file.ext',
    'http://www.loudoun.k12.va.us/page/101110',
    'http://www.youtube.com/channel/UCeY0bbntWzzVIaj2z3QigXg',
    'http://www.arborday.org/Trees/treeguide/TreeDetail.cfm?ItemID=861',
    'http://www.arborday.org/Trees/treeguide/TreeDetail.cfm?ItemID=861&zpid=1&ypid=3',
    'http://www.instagram.com/p/',

    'https://crowfly.net',
    'https://dev.crowfly.net',
    'https://dev.crowfly.net/',
    'https://dev.crowfly.net/a_file.ext',
    'https://dev.crowfly.net/a_file.ext.ext2',
    'https://dev.crowfly.net/foo',
    'https://dev.crowfly.net/foo/bar',
    'https://dev.crowfly.net/foo/bar/baz',
    'https://dev.crowfly.net/foo/bar/baz/a_file.ext',
    'https://www.loudoun.k12.va.us/page/101110',
    'https://www.youtube.com/channel/UCeY0bbntWzzVIaj2z3QigXg',
    'https://www.arborday.org/Trees/treeguide/TreeDetail.cfm?ItemID=861',
    'https://www.arborday.org/Trees/treeguide/TreeDetail.cfm?ItemID=861&zpid=1&ypid=3',
    'https://www.instagram.com/p/',
    ]

TEST_TEXT = 'Hello %s, howdie?'


TEST_TEXT_MULTIPLE_URLS = \
    "Nearly all men can stand adversity %s, but if you want to test a man's character %s, give him power %s."

TEST_TEXT_RESULTS_WITH_TARGET = \
    'Hello <a href="http://crowfly.net" target="_blank">crowfly.net</a>, howdie?'


class TestUrls(unittest.TestCase):

    def setUp(self):
        self.urls = Urls()

    def test_makeLinksHot(self):

        for i, url in enumerate(TEST_URLS):
            text = TEST_TEXT % url
            result = self.urls.makeLinksHot(text)
            self.assertTrue('<a href=' in result)

    def test_makeLinksHot_recursion(self):
        # get 3 urls:
        url1, url2, url3 = TEST_URLS[0:3]

        # compile text with three urls inserged:
        text = TEST_TEXT_MULTIPLE_URLS % (url1, url2, url3)

        result = self.urls.makeLinksHot(text)
        self.assertEqual(result.count('<a href='), 3)

    def test_makeLinksHot_with_target(self):
        urls2 = Urls(target='_blank')

        url = TEST_URLS[0]
        text = TEST_TEXT % url
        result = urls2.makeLinksHot(text)
        self.assertEqual(result, TEST_TEXT_RESULTS_WITH_TARGET)

    def test_makeLinksHot_dashes(self):
        text = 'https://edsource.org/topic/college-careers'
        reference = '<a href="https://edsource.org/topic/college-careers">https://edsource.org/topic/college-careers</a>'
        result = self.urls.makeLinksHot(text)
        self.assertEqual(result, reference)

    def test_makeLinksHot_wrong(self):
        text = 'The meeting will be held at 7 p.m. in the School Board Meeting Room.'
        reference = text
        result = self.urls.makeLinksHot(text)
        self.assertEqual(result, reference)

if __name__ == '__main__':
    unittest.main()
