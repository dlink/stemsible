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

    @lazyproperty
    def users(self): return __import__('users').Users()

    def __init__(self):
        self.logger = logger.getLogger(self.__class__.__name__)
        self.notifications = Notifications()

    def run(self):
        '''Set up Command Line (CLI) commands and options launch CLI process
        '''
        commands = ['email message_activity [user_email]',
                    'email summary [user_email]',
                    'show missing_school_addresses']
        options = {'y': "Answer yes to prompts"}

        self.cli = CLI(self.process, commands, options)
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

        elif cmd == 'email':
            validate_num_args('email', 1, args)
            target = args.pop(0)
            user = self.users.getUsers({'email':args.pop(0)})[0] \
                   if args else None

            if target == 'message_activity':
                self.notifications.sendMessageActivity(user)
            elif target == 'summary':
                self.notifications.sendSummary(user)
            else:
                raise StemsibleArgsError('Unrecognized email target: %s'
                                         % target)
        else:
            raise StemsibleArgsError('Unrecognized command: %s' % cmd)

if __name__ == '__main__':
    Stemsible().run()
