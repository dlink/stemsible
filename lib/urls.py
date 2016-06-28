#!/usr/bin/env python

from jinja2.utils import urlize


class Urls(object):
    '''Preside over URLs'''

    def __init__(self, target=None):
        self.target = target

    def makeLinksHot(self, text):
        return urlize(text, target=self.target)

if __name__ == '__main__':
    import sys
    u = Urls()
    print u.makeLinksHot(sys.argv[1])
