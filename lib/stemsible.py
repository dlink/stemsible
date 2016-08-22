#!/usr/bin/env python

from vlib import logger
from vlib.utils import lazyproperty, validate_num_args
from vlib.cli import CLI
from notifications import Notifications


class StemsibleError(Exception): pass
class StemsibleArgsError(StemsibleError): pass

class Stemsible(object):
    '''Stemsible CLI engine'''

    @lazyproperty
    def schools(self): return __import__('schools').Schools()

    def __init__(self):
        self.logger = logger.getLogger(self.__class__.__name__)
        self.notifications = Notifications()

    def run(self):
        '''Set up Command Line (CLI) commands and options launch CLI process
        '''
        commands = ['send_user_notifications',
                    'show missing_school_addresses']

        self.cli = CLI(self.process, commands)
        self.cli.process()

    def process(self, *args):
        '''Process all Incoming Requests
           Implement a catch all Exceptions
           Log any Errors

           Return status of process as a string
        '''
        args = list(args)
        signature = 'stemsible.py ' + ' '.join(args)
        try:
            return self._process(args)
        except Exception, e:
            emsg = '%s: %s: %s' % (e.__class__.__name__, signature, e)
            self.logger.error(emsg)
            raise

    def _process(self, args):
        '''Called by process() to do its work
           Return status of process as a string
        '''
        cmd = args.pop(0)
        if cmd == 'show':
            validate_num_args('show', 1, args)
            target = args.pop(0)
            if target == 'missing_school_addresses':
                return self.schools.missingAddresses()
            else:
                return StemsibleArgsError('Unrecognized show target: %s'
                                          % target)
            print target

        elif cmd == 'send_user_notifications':
            self.notifications.emailNotification()
        else:
            raise StemsibleArgsError('Unrecognized command: %s' % cmd)

if __name__ == '__main__':
    Stemsible().run()
