#!/usr/bin/env python

from vlib import db
from vlib import conf
from vlib.cli import CLI, CLI_Error

class Search(object):

    def __init__(self):
        self.db = db.getInstance()
        self.conf = conf.getInstance()

    def run(self):
        commands = ['reindex']
        self.cli = CLI(self.process, commands)
        print self.cli.process()

    def process(self, *args):
        '''Process incoming requests'''
        args = list(args)

        #if len(args) < 1:
        #    self.cli.syntax('missing args')

        cmd = args.pop(0)
        if cmd == 'reindex':
            return self.reIndex()

        else:
            raise CLI_Error('Unrecognized Command: %s' % cmd)


    def reIndex(self):
        file = '%s/lib/sql/create_messages_flat.sql' % self.conf.basedir
        sql_cmds = open(file, 'r').read().split(';')

        rowcount = 0
        for sql in sql_cmds:
            if sql.strip():
                self.db.execute(sql)
                if 'create table' in sql:
                    rowcount = self.db.rowcount
        return '%s search message reindex' % rowcount

if __name__ == '__main__':
    Search().run()
