from vlib import db

from record import Record
from users import User

DEBUG = 1

# some fixed messages:
from vlib.odict import odict
MESSAGES = [odict(id=1, user_id=1, created='12 hrs', text='hello there'),
            odict(id=2, user_id=5, created='Yesterday at 2:10 pm',
                  text='Nice day mate'),
            odict(id=3, user_id=2, created='Yesterday at 1:13 pm',
                  text='Before you can store Messages, we need to create a full database schema, and create the database'),
            odict(id=3, user_id=3, created='Yesterday at 8:34 am',
                  text="Ever since Lincoln wrote it in 1864, this version has been the most often reproduced, notably on the walls of the Lincoln Memorial in Washington. It is named after Colonel Alexander Bliss, stepson of historian George Bancroft. Bancroft asked President Lincoln for a copy to use as a fundraiser for soldiers (see \"Bancroft Copy\" below). However, because Lincoln wrote on both sides of the paper, the speech could not be reprinted, so Lincoln made another copy at Bliss's request. It is the last known copy written by Lincoln and the only one signed and dated by him. Today it is on display at the Lincoln Room of the White House.")]

class Messages(object):

    def get(self):
        o = []
        for m in MESSAGES:
            o.append(Message(m))
        return o

class Message(Record):
    '''Preside over a single Message'''

    def __init__(self, id):
        '''Create a Message Object given a message_id'''
        Record.__init__(self, db.getInstance(), 'messages', id)
