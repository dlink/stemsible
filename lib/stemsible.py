#!/usr/bin/env python

from vlib import logger
from vlib.utils import validate_num_args
from vlib.cli import CLI
from notifications import Notifications


class StemsibleError(Exception): pass
class StemsibleArgsError(StemsibleError): pass

class Stemsible(object):
    '''Stemsible CLI engine'''

    def __init__(self):
        self.logger = logger.getLogger(self.__class__.__name__)
        self.notifications = Notifications()

    def run(self):
        '''Set up Command Line (CLI) commands and options launch CLI process
        '''
        commands = ['send_user_notifications']
        self.cli = CLI(self.process, commands)
        self.cli.process()

    def process(self, args):
        '''Process all Incoming Requests
           Implement a catch all Exceptions
           Log any Errors

           Return status of process as a string
        '''
        signature = 'stemsible.py ' + args
        try:
            return self._process([args])
        except Exception, e:
            emsg = '%s: %s: %s' % (e.__class__.__name__, signature, e)
            self.logger.error(emsg)
            raise

    def _process(self, *args):
        '''Called by process() to do its work
           Return status of process as a string
        '''
        cmd = args[0][0]
        if cmd == 'send_user_notifications':
            self.notifications.emailNotification()
        else:
            raise StemsibleArgsError('Unrecognized command: %s' % cmd)

if __name__ == '__main__':
    Stemsible().run()
