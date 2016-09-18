#!/usr/bin/env python

import re

URL_RE = r'https?://[^\s]+'

class Urls(object):
    '''Preside over URLs'''

    def __init__(self, target=None):
        self.parser = re.compile(URL_RE, re.VERBOSE)

    def extractUrls(self, text, urls=None):
        '''Given a string, return a list of all URLs'''
        
        if not urls:
            urls = []

        match = self.parser.search(text)
        if not match:
            return urls        
        p,q = match.span()
        urls.append(text[p:q])
        return self.extractUrls(text[q:], urls)

if __name__ == '__main__':
    import sys
    u = Urls()
    print u.extractUrls('this is a test: https://crowfly.net and '
                        'http://stemsible.com/abc/abc=asdfasf')

