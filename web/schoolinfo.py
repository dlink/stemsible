
from vweb.htmltable import HtmlTable
from vweb.html import *

from grades import Grades
from schoolrelationships import SchoolRelationships
from registration import Registration

class SchoolInfo(object):

    def __init__(self):
        self.add_school_row = 0

        self.school = ''
        self.school_rel = 0
        self.grade = 0
        self.missing_values = []

    def getCssFile(self):
        return ['css/schoolinfo.css'] #, 'css/signup.css']

    def getJsFile(self):
        return ['js/schoolinfo.js', 'js/typeahead.js']

    def process(self, session, form):
        self.session = session
        self.form = form

        # add school row?
        if 'add_school_row' in self.form:
            self.add_school_row = 1

        # save new school?
        if 'save_new_school' in self.form:

            for f in ['school', 'school_rel', 'grade']:
                if f in self.form and self.form[f].value:
                    self.__dict__[f] = self.form[f].value
                else:
                    self.missing_values.append(f)

            if not self.missing_values:
                Registration().addSchool(self.session.user,
                                         self.form['school_rel'].value,
                                         self.form['school'].value,
                                         self.form['grade'].value)
            else:
                self.add_school_row = 1

        # delete user_school
        if 'delete_user_school' in self.form:
            from userschools import UserSchools
            UserSchools().delete(self.form['delete_user_school'].value)

    def getHtml(self, user):
        can_edit = user.id == self.session.user.id

        header = h3('School Information')
        #help = span(a('Why do I need to provide this information?'),
        #            class_='helpMsg',
        #            title='By knowing what school or schools you are '
        #            'interested in, we can provide you with conversations '
        #            'that are meaningful to you.')

        table = HtmlTable(class_='table')

        # header
        col_header = ['Role', 'School', 'Grade']
        if can_edit:
            col_header.append('&nbsp;')
        table.addHeader(col_header)

        # schools
        for s in user.schools:
            row = [s['relation'], s['school'], s['grade']]
            row[2] = Grades().table[row[2]]['name']
            if can_edit:
                school_info = '%s - %s - %s Grade' % tuple(row)
                row.append(a('X', class_ = 'delete',
                             onclick="javascript:deleteSchool(%s, '%s');"
                             % (s['id'], school_info)))
            table.addRow(row)
            table.setColClass(3, 'right-center')

        # add school row
        if self.add_school_row:
            table.addRow(self.schoolFields())

        # buttons
        buttons = ''
        if can_edit:

            # [add new school] button
            if not self.add_school_row:
                add_button = a('Add another school',
                               class_='btn btn-primary first-button',
                               onClick='javascript:addSchoolRow();')
                buttons += add_button

            # [save] + [cancel] buttons
            if self.add_school_row:
                save_button = a('Save',
                                class_='btn btn-success first-button',
                                onClick='javascript:saveNewSchool()')
                cancel_button = a('Cancel', class_='btn btn-warning',
                                  onclick="location.href='profile.py';")
                buttons += save_button + cancel_button

        # hidden fields
        hidden_fields = \
            input(type='hidden', name='add_school_row') + \
            input(type='hidden', name='save_new_school') + \
            input(type='hidden', name='delete_user_school')


        body = div(table.getTable() + buttons + hidden_fields,
                   id='schoolInfo')
        return header + form(body, name='si_form', method='POST')
    '''
        return header + \
            div(
                table.getTable() + \
                buttons + \
                hidden_fields,
            id='schoolInfo')
            '''
    def schoolFields(self):
        '''Return a the three fields as list'''
        # Fields
        return [p(b('Add a School:')) + \
                    self._schoolRelField(),
                self._schoolField(),
                self._gradeField()]

    def _schoolRelField(self):
        '''Build school relationship field'''
        options = {0: 'Select one'}
        for id, record in SchoolRelationships().table.items():
            options[id] = record['description']
        return self.mkDropDownMenu('school_rel', options)

    def _schoolField(self):
        '''Build school name field'''
        class_ = 'typeahead form-control'
        if 'school' in self.missing_values:
            class_ += ' missing-value'
        return div(input(name='school', placeholder='School Name',
                         value=self.school, class_=class_), id='school')

    def _gradeField(self):
        '''Build school grade field'''
        options = {0: 'Select grade'}
        for id, record in Grades().table.items():
            options[id] = record['name']
        return self.mkDropDownMenu('grade', options)

    def mkDropDownMenu(self, name, options):
        '''Build an HTML drop down menu field'''

        class_ = 'dropdown form-control'
        if name in self.missing_values:
            class_ += ' missing-value'
        #if name == 'school_rel':
        #    class_ += ' long'
        attrs = {'class_': class_}

        # sort ids, but put 0 on top
        ids = sorted(options.keys())
        p = ids.index(0)
        ids = [0] + ids[0:p] + ids[p+1:]

        # build select
        options_html = ''
        i = 0
        for id in ids:
            desc = options[id]
            option_attrs = {}
            if i == 0:
                option_attrs['disabled'] = 1
            if int(self.__dict__[name]) == id:
                option_attrs['selected'] = 1
            options_html += option(desc, value=id, **option_attrs) + '\n'
            i += 1
        return select(options_html, name=name, **attrs)
