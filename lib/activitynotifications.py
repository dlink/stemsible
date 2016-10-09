from vlib import conf, db, logger

class ActivityNotifications(object):

    def __init__(self):
        self.conf = conf.getInstance() 
        self.db = db.getInstance()
        self.logger = logger.getLogger(self.__class__.__name__)
        
    def registerComment(self, comment_data):
        '''Given comment message data as a DICT
           queue up activity notifications to everyone
           involved in the original message. (author, commenters and likers)
        '''
        user_id    = comment_data['user_id']
        comment_id = comment_data['id']
        message_id = comment_data['reference_id']

        sql_file = '%s/lib/sql/register_comments.sql' % self.conf.basedir
        sql = open(sql_file, 'r').read().format(user_id=user_id,
                                                comment_id=comment_id,
                                                message_id=message_id)
        self.db.execute(sql)
    
