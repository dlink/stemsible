#!/usr/bin/env python

#from vlib.odict import odict

#from vweb.html import *
#from vweb.htmlpage import HtmlPage
import json

from vlib import conf
from messages import Messages

class MessagesApi():

    def __init__(self):
        #HtmlPage.__init__(self, 'Messages')
        self.conf = conf.getInstance()
        self.messages = Messages()

    def go(self):
        return \
            'Content-Type: application/json\n\n' + \
            self.getMessages()

    def getMessages(self):
        messages = Messages()
        messages.setColumns(['id', 'user_id', 'text', 'created'])
        messages.setOrderBy('id')
        #messages.setLimit(1)
        results = messages.getTable()
        data = {
            'messages': [
                {'id'      : r['id'],
                 'user_id' : r['user_id'],
                 'text'    : r['text'],
                 'created' : str(r['created']),
                 'uri': 'http://%s/messages/%s' % (self.conf.serverurl, r['id']),
                 }
                for r in results]
            }
        return json.dumps(data)

if __name__ == '__main__':
    print MessagesApi().go()
