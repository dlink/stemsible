#!/usr/bin/env python

import re

URL_RE = r'''
                             # Prototype
  ((http|https)://)?         #     http:// | https://     - optional

                             # Domain
  \w{1,20}(\.\w{1,20}){1,3}  #     abc.def .. abc.def.hij.klm

                             # Subdirectories
  (/\W                       #    lone tailing / or url   - optional
    |                        #        - or -
   /\w{1,20}                 #    subdir
   (/\w{1,20}){0,3}          #    and/or multiple subdirs - optional
  )?

                             # Filename Extention
  (\.\w{1,20}){0,2}          #    abc .. abc.def.hij      - optional
'''
class Urls(object):
    '''Preside over URLs'''

    def __init__(self, target=None):
        self.parser = re.compile(URL_RE, re.VERBOSE)

        self.target_phrase = ''
        if target:
            self.target_phrase = ' target="%s"' % target

    def makeLinksHot(self, text):
        '''Replace all urls in a string with html anchor tags (links)

           eq.:
                 Checkout crowfly.net!
           becomes:
                 Checkout <a href="crowfly.net">crowfly.net</a>!
        '''
        match = self.parser.search(text)
        if not match:
            return text

        p, q = match.span()
        url = url2 = text[p:q]
        if not url.startswith('http'):
            url2 = 'http://' + url

        link = '<a href="{url2}"{target_phrase}>{url}</a>'\
            .format(url=url, url2=url2, target_phrase=self.target_phrase)

        text2 = \
            text[0:p] + \
            link + \
            self.makeLinksHot(text[q:])
        return text2

if __name__ == '__main__':
    import sys
    u = Urls()
    print u.makeLinksHot(sys.argv[1])

