
from vweb.html import *

class Header(object):

    def __init__(self, page_name):
        self.page_name = page_name

    def getHtml(self):
        return p(self.page_name)
