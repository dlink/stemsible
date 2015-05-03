
from vlib.odict import odict

class Messages(object):

    def get(self):
        return [Message(odict(id=1, text='hello there')),
                Message(odict(id=2, text='Nice day mate')),
                Message(odict(id=3, text='Before you can store Messages, we need to create a full database schema, and create the database')),
                Message(odict(id=3, text="Ever since Lincoln wrote it in 1864, this version has been the most often reproduced, notably on the walls of the Lincoln Memorial in Washington. It is named after Colonel Alexander Bliss, stepson of historian George Bancroft. Bancroft asked President Lincoln for a copy to use as a fundraiser for soldiers (see \"Bancroft Copy\" below). However, because Lincoln wrote on both sides of the paper, the speech could not be reprinted, so Lincoln made another copy at Bliss's request. It is the last known copy written by Lincoln and the only one signed and dated by him. Today it is on display at the Lincoln Room of the White House."))]
        
class Message(object):

    def __init__(self, data):
        self.id = data.id
        self.text = data.text
