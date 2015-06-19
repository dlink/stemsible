#!/usr/bin/env python

#from vlib.odict import odict

#from vweb.html import *
#from vweb.htmlpage import HtmlPage
import cgi
#import cgitb
#cgitb.enable()
import json

from vlib import conf
from messages import Messages

class MessagesApi(object):

    def __init__(self):
        log('init')
        self.conf = conf.getInstance()
        self.messages = Messages()

        # process
        #print \
        #    'Content-Type: text/html\n\n'

        self.form = cgi.FieldStorage()
        log('self.form:' + str(self.form) + str(type(self.form)))

        
    def go(self):
        log('go')
        log('self.form:' + str(self.form))
        #log('d:', self.form['data'].value)
        #log('cond:' + str('data' in self.form))
        for p in self.form:
            log('p:' + self.form['p'].value)
        log ('here')
        if 'data' in self.form:
            #results =  self.addMessages(self.form['data'].value)
            results = self.addMessage({'text': 'testing x123', 'user_id': 1})
        else:
            results = self.getMessages()

        return \
            'Content-Type: application/json\n\n' + \
            results

    def getMessages(self):
        messages = Messages()
        messages.setColumns(['id', 'user_id', 'text', 'created'])
        messages.setOrderBy('id desc')
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

    def addMessage(self, data):
        log('hi');
        messages = Messages()
        messages.insertRow(data)
        return 'Added'

def log(m):
    fp = open('/tmp/a.log', 'a')
    fp.write(m + '\n')
    fp.close()

if __name__ == '__main__':
    print MessagesApi().go()
