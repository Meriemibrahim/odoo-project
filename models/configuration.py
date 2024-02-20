
import calendar
import re

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.translate import _

class AcademicYear(models.Model):

    _name = "academic.year"
    _description = "Academic Year"
    _order = "sequence"

    sequence = fields.Integer('Sequence', required=True,
                              help="Sequence order you want to see this year.")
    name = fields.Char('Name', required=True, help='Name of academic year')
    code = fields.Char('Code', required=True, help='Code of academic year')
    date_start = fields.Date('Start Date', required=True,
                             help='Starting date of academic year')
    date_stop = fields.Date('End Date', required=True,
                            help='Ending of academic year')

    current = fields.Boolean('Current', help="Set Active Current Year")
    description = fields.Text('Description', help='Description')





    @api.constrains('date_start', 'date_stop')
    def _check_academic_year(self):

        new_start_date = self.date_start
        new_stop_date = self.date_stop
        delta = new_stop_date - new_start_date
        if delta.days > 365 and not calendar.isleap(new_start_date.year):
            raise ValidationError(_(
                "The duration of the academic year is invalid."))
        if (self.date_stop and self.date_start and
                self.date_stop < self.date_start):
            raise ValidationError(_(
                "The start date of the academic year should be less than end date."))
        for old_ac in self.search([('id', 'not in', self.ids)]):
            if (old_ac.date_start <= self.date_start <= old_ac.date_stop or
                    old_ac.date_start <= self.date_stop <= old_ac.date_stop):
                raise ValidationError(_(
                    "Error! You cannot define overlapping academic years."))

    @api.constrains('current')
    def check_current_year(self):
        current_year_rec = self.search_count([('current', '=', True)])
        if current_year_rec >= 2:
            raise ValidationError(_(
                "Error! You cannot set two current year active!"))

    @api.constrains('date_start', 'date_stop')
    def _check_academic_year(self):

        new_start_date = self.date_start
        new_stop_date = self.date_stop
        delta = new_stop_date - new_start_date
        if delta.days > 365 and not calendar.isleap(new_start_date.year):
            raise ValidationError(_(
                "The duration of the academic year is invalid."))
        if (self.date_stop and self.date_start and
                self.date_stop < self.date_start):
            raise ValidationError(_(
                "The start date of the academic year should be less than end date."))
        for old_ac in self.search([('id', 'not in', self.ids)]):
            # Check start date should be less than stop date
            if (old_ac.date_start <= self.date_start <= old_ac.date_stop or
                    old_ac.date_start <= self.date_stop <= old_ac.date_stop):
                raise ValidationError(_(
                    "Error! You cannot define overlapping academic years."))
#
    @api.constrains('current')
    def check_current_year(self):
        '''Constraint on active current year'''
        current_year_rec = self.search_count([('current', '=', True)])
        if current_year_rec >= 2:
            raise ValidationError(_(
                "Error! You cannot set two current year active!"))

class SpecialitySpeciality(models.Model):

    _name = "class.speciality"
    _description = "class.speciality"
    _order = "no"

    no = fields.Integer('no', required=True,
                              help='no of the record')
    name = fields.Char('Name', required=True,
                       help='speciality of class')
    code = fields.Char('Code', required=True,
                       help='speciality code')
    description = fields.Text('Description', help='Description')


class ClassNiveau(models.Model):

    _name = "class.niveau"
    _description = "class.niveau"
    _order = "no"

    no = fields.Integer('no', required=True,
                              help='no of the record')
    name = fields.Char('Name', required=True,
                       help='niveau of the school')
    code = fields.Char('Code', required=True,
                       help='niveau code')
    description = fields.Text('Description', help='Description')



class SchoolSchool(models.Model):

    _name = 'school.school'
    _description = 'School Information'
    _rec_name = "com_name"

    @api.model
    def _lang_get(self):
        languages = self.env['res.lang'].search([])
        return [(language.code, language.name) for language in languages]

    company_id = fields.Many2one('res.company', 'Company', ondelete="cascade",
                                 required=True, delegate=True,
                                 help='Company_id of the school')
    com_name = fields.Char('School Name', related='company_id.name',
                           store=True, help='School name')
    code = fields.Char('Code', required=True, help='School code')
    class_room = fields.One2many('class.room', 'school_id',
                                'classe', help='school classe')
    lang = fields.Selection(_lang_get, 'Language',
                            help='''If the selected language is loaded in the
                                system, all documents related to this partner
                                will be printed in this language.
                                If not, it will be English.''')
    required_age = fields.Integer("Student Admission Age Required", default=6,
                                  help='''Minimum required age for
                                  student admission''')

    @api.model
    def create(self, vals):
        res = super(SchoolSchool, self).create(vals)
        main_company = self.env.ref('base.main_company')
        res.company_id.parent_id = main_company.id
        return res



class prix(models.Model):

    _name = 'prix.prix'
    _description = "prix"

    prix_list_id = fields.Many2one('student.student', 'Student',
                                    help='student how get it!')
    name = fields.Char('prix Name', help='prix name')
    description = fields.Char('Description', help='Description')





class StudentDocument(models.Model):
    _name = 'student.document'
    _description = "Student Document"
    _rec_name = "doc_type"

    doc_id = fields.Many2one('student.student', 'Student',
                             help='Student of the following doc')
    file_no = fields.Char('File No', readonly="1",
                          default=lambda obj: obj.env[
                              'ir.sequence'].next_by_code('student.document'),
                          help='File no of the document')
    submited_date = fields.Date('Submitted Date',
                                help='Document submitted date')
    doc_type = fields.Many2one('document.type', 'Document Type', required=True,
                               help='Document type')
    file_name = fields.Char('File Name', help='File name')
    return_date = fields.Date('Return Date', help='Document return date')
    new_datas = fields.Binary('Attachments', help='Attachments of the document')





class DocumentType(models.Model):
    _name = "document.type"
    _description = "Document Type"
    _rec_name = "doc_type"
    _order = "seq_no"

    seq_no = fields.Char('Sequence', readonly=True,
                         default=lambda self: _('New'),
                         help='Sequence of the document')
    doc_type = fields.Char('Document Type', required=True,
                           help='Document type')

    @api.model
    def create(self, vals):
        if vals.get('seq_no', _('New')) == _('New'):
            vals['seq_no'] = self.env['ir.sequence'].next_by_code(
                'document.type') or _('New')
        return super(DocumentType, self).create(vals)




class StudentDescription(models.Model):
    _name = 'student.description'
    _description = "Student Description"

    des_id = fields.Many2one('student.student', 'Student Ref.',
                             help='Student record from students')
    name = fields.Char('Name', help='Description name')
    description = fields.Char('Description', help='Student description')








class StudentCertificate(models.Model):

    _name = "student.certificate"
    _description = "Student Certificate"

    student_id = fields.Many2one('student.student', 'Student',
                                 help='Related student')
    description = fields.Char('Description', help='Description')
    certi = fields.Binary('Certificate', required=True,
                          help='Student certificate')


