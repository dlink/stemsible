#!/usr/bin/env python

from datetime import datetime
import unittest

from urls import Urls

# Fixtures

TEST_URLS = [
    'crowfly.net',
    'dev.crowfly.net',
    'dev.crowfly.net/',
    'dev.crowfly.net/a_file.ext',
    'dev.crowfly.net/a_file.ext.ext2',
    'dev.crowfly.net/foo',
    'dev.crowfly.net/foo/bar',
    'dev.crowfly.net/foo/bar/baz',
    'dev.crowfly.net/foo/bar/baz/a_file.ext',

    'http://crowfly.net',
    'http://dev.crowfly.net',
    'http://dev.crowfly.net/',
    'http://dev.crowfly.net/a_file.ext',
    'http://dev.crowfly.net/a_file.ext.ext2',
    'http://dev.crowfly.net/foo',
    'http://dev.crowfly.net/foo/bar',
    'http://dev.crowfly.net/foo/bar/baz',
    'http://dev.crowfly.net/foo/bar/baz/a_file.ext',

    'https://crowfly.net',
    'https://dev.crowfly.net',
    'https://dev.crowfly.net/',
    'https://dev.crowfly.net/a_file.ext',
    'https://dev.crowfly.net/a_file.ext.ext2',
    'https://dev.crowfly.net/foo',
    'https://dev.crowfly.net/foo/bar',
    'https://dev.crowfly.net/foo/bar/baz',
    'https://dev.crowfly.net/foo/bar/baz/a_file.ext',
    ]

TEST_TEXT = 'Hello %s, howdie?'
TEST_TEXT_RESULTS = [
    'Hello <a href="http://crowfly.net">crowfly.net</a>, howdie?',
    'Hello <a href="http://dev.crowfly.net">dev.crowfly.net</a>, howdie?',
    'Hello <a href="http://dev.crowfly.net/,">dev.crowfly.net/,</a> howdie?',
    'Hello <a href="http://dev.crowfly.net/a_file.ext">dev.crowfly.net/a_file.ext</a>, howdie?',
    'Hello <a href="http://dev.crowfly.net/a_file.ext.ext2">dev.crowfly.net/a_file.ext.ext2</a>, howdie?',
    'Hello <a href="http://dev.crowfly.net/foo">dev.crowfly.net/foo</a>, howdie?',
    'Hello <a href="http://dev.crowfly.net/foo/bar">dev.crowfly.net/foo/bar</a>, howdie?',
    'Hello <a href="http://dev.crowfly.net/foo/bar/baz">dev.crowfly.net/foo/bar/baz</a>, howdie?',
    'Hello <a href="http://dev.crowfly.net/foo/bar/baz/a_file.ext">dev.crowfly.net/foo/bar/baz/a_file.ext</a>, howdie?',
    'Hello <a href="http://crowfly.net">http://crowfly.net</a>, howdie?',
    'Hello <a href="http://dev.crowfly.net">http://dev.crowfly.net</a>, howdie?',
    'Hello <a href="http://dev.crowfly.net/,">http://dev.crowfly.net/,</a> howdie?',
    'Hello <a href="http://dev.crowfly.net/a_file.ext">http://dev.crowfly.net/a_file.ext</a>, howdie?',
    'Hello <a href="http://dev.crowfly.net/a_file.ext.ext2">http://dev.crowfly.net/a_file.ext.ext2</a>, howdie?',
    'Hello <a href="http://dev.crowfly.net/foo">http://dev.crowfly.net/foo</a>, howdie?',
    'Hello <a href="http://dev.crowfly.net/foo/bar">http://dev.crowfly.net/foo/bar</a>, howdie?',
    'Hello <a href="http://dev.crowfly.net/foo/bar/baz">http://dev.crowfly.net/foo/bar/baz</a>, howdie?',
    'Hello <a href="http://dev.crowfly.net/foo/bar/baz/a_file.ext">http://dev.crowfly.net/foo/bar/baz/a_file.ext</a>, howdie?',
    'Hello <a href="https://crowfly.net">https://crowfly.net</a>, howdie?',
    'Hello <a href="https://dev.crowfly.net">https://dev.crowfly.net</a>, howdie?',
    'Hello <a href="https://dev.crowfly.net/,">https://dev.crowfly.net/,</a> howdie?',
    'Hello <a href="https://dev.crowfly.net/a_file.ext">https://dev.crowfly.net/a_file.ext</a>, howdie?',
    'Hello <a href="https://dev.crowfly.net/a_file.ext.ext2">https://dev.crowfly.net/a_file.ext.ext2</a>, howdie?',
    'Hello <a href="https://dev.crowfly.net/foo">https://dev.crowfly.net/foo</a>, howdie?',
    'Hello <a href="https://dev.crowfly.net/foo/bar">https://dev.crowfly.net/foo/bar</a>, howdie?',
    'Hello <a href="https://dev.crowfly.net/foo/bar/baz">https://dev.crowfly.net/foo/bar/baz</a>, howdie?',
    'Hello <a href="https://dev.crowfly.net/foo/bar/baz/a_file.ext">https://dev.crowfly.net/foo/bar/baz/a_file.ext</a>, howdie?',
    ]

TEST_TEXT_MULTIPLE_URLS = \
    "Nearly all men can stand adversity %s, but if you want to test a man's character %s, give him power %s."

TEST_TEXT_MULTIPLE_URLS_RESULTS = \
    '''Nearly all men can stand adversity <a href="http://crowfly.net">crowfly.net</a>, but if you want to test a man's character <a href="http://dev.crowfly.net">dev.crowfly.net</a>, give him power <a href="http://dev.crowfly.net/.">dev.crowfly.net/.</a>'''

TEST_TEXT_RESULTS_WITH_TARGET = \
    'Hello <a href="http://crowfly.net" target="_blank">crowfly.net</a>, howdie?'

class TestUrls(unittest.TestCase):
    '''Test Urls'''

    def setUp(self):
        self.urls = Urls()

    def test_makeLinksHot(self):

        for i, url in enumerate(TEST_URLS):
            text = TEST_TEXT % url
            result = self.urls.makeLinksHot(text)
            #print result
            self.assertEqual(result, TEST_TEXT_RESULTS[i])


    def test_makeLinksHot_recursion(self):
        # get 3 urls:
        url1, url2, url3 = TEST_URLS[0:3]

        # compile text with three urls inserged:
        text = TEST_TEXT_MULTIPLE_URLS % (url1, url2, url3)

        result = self.urls.makeLinksHot(text)
        #print result
        self.assertEqual(result, TEST_TEXT_MULTIPLE_URLS_RESULTS)


    def test_makeLinksHot_with_target(self):
        urls2 = Urls(target='_blank')

        url = TEST_URLS[0]
        text = TEST_TEXT % url
        result = urls2.makeLinksHot(text)
        #print result
        self.assertEqual(result, TEST_TEXT_RESULTS_WITH_TARGET)

if __name__ == '__main__':
    unittest.main()
