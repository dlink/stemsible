from passlib.hash import sha256_crypt

from vlib import db
from vlib import logger
from vlib.utils import lazyproperty

from users import Users
from userschools import UserSchools
from follows import Follows
from schools import Schools, UNKNOWN_ADDRESS_ID, UNKNOWN_DISTRICT_ID


class Registration(object):

    @lazyproperty
    def logger(self):
        return logger.getLogger('Registration')

    def __init__(self):
        self.db = db.getInstance()

    def add(self, user_data, user_school_data):
        '''Writes to users, user_schools, follows, and possibly
                     schools database tables

           Expects two dictionaries

              user_data, with keys:
                 first_name, last_name, email, password, status_id

              user_school_data, with keys:
                 school_name, school_relationship_id, original_grade
        '''
        self.db.startTransaction()
        try:
            user_data['password'] = sha256_crypt.encrypt(user_data['password'])
            user = Users().add(user_data)

            # get school_id
            school_name = user_school_data['school_name']
            school_id = self._getSchoolId(school_name)

            # set user_school_rec
            user_school_rec = user_school_data
            user_school_rec['user_id'] = user.id
            user_school_rec['school_id'] = school_id
            user_school_rec['grade'] = user_school_data['original_grade']
            del user_school_rec['school_name']
            UserSchools().add(user_school_rec)

            # set user followings
            Follows().update(user)

            self.db.commit()
        except Exception, e:
            emsg = \
                'Unable to register user: user_data: %s; ' \
                'user_school_data: %s; Error: %s' \
                % (user_data, user_school_data, e)
            self.logger.error(emsg)
            self.db.rollback()
            raise

        self.logger.info('New Registration: %s, %s' % (user.id, user.fullname))

    def addSchool(self, user, school_rel_id, school_name, grade):
        self.db.startTransaction()
        try:
            # get school_id
            school_id = self._getSchoolId(school_name)

            # set user_school_rec
            rec = {'user_id': user.id,
                   'school_relationship_id': school_rel_id,
                   'school_id': school_id,
                   'grade': grade,
                   'original_grade': grade,
                   'active': 1}
            UserSchools().add(rec)
            self.db.commit()
        except Exception, e:
            emsg = \
                'Unable to add School: %s; Error: %s' % (school_name, e)
            self.logger.error(emsg)
            self.db.rollback()
            raise

        self.logger.info('Added School: {0}, {1}, {2}'
                         .format(user.id, user.fullname, school_name))

    def _getSchoolId(self, school_name):
        '''Given a school name
           Create a new school record if nec. (with unknown District and addr)
           Return school id
        '''
        sql = 'select id from schools where name = %s'
        results = self.db.query(sql, params=[school_name])
        if results:
            school_id = results[0]['id']
        else:
            # create new School Record with Unknown Values
            school_rec = {'school_district_id': UNKNOWN_DISTRICT_ID,
                          'code': '',
                          'name': school_name,
                          'active': 1,
                          'address_id': UNKNOWN_ADDRESS_ID}
            school = Schools().add(school_rec)
            school_id = school['id']
            self.logger.info('Added School: %s, %s' % (school_id, school_name))
        return school_id
