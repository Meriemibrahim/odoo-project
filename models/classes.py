import calendar
import re

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.translate import _


class ClassRoom(models.Model):
    _name = 'class.room'
    _description = 'Students'
    _rec_name = "speciality_id"

    name = fields.Char("name")
    email = fields.Char("EMAIL")

    @api.depends('speciality_id', 'school_id', 'niveau_id',
                 )
    def _compute_student(self):
        student_obj = self.env['student.student']
        for rec in self:
            rec.student_ids = student_obj. \
                search([('speciality_id', '=', rec.id),
                        ('school_id', '=', rec.school_id.id),
                        ('niveau_id', '=', rec.niveau_id.id),

                        ])

    @api.depends('matiere_ids')
    def _compute_matiere(self):
        for rec in self:
            rec.total_no_matiere = len(rec.matiere.ids)

    @api.depends('student_ids')
    def _compute_total_student(self):
        for rec in self:
            rec.total_students = len(rec.student_ids)

    @api.depends("capacity", "total_students")
    def _compute_remain_seats(self):
        for rec in self:
            rec.remaining_seats = rec.capacity - rec.total_students

    school_id = fields.Many2one('school.school', 'School', required=True,
                                help='School of the following standard')
    speciality_id = fields.Many2one('class.speciality', 'speciality',
                                    required=True, help='Standard')
    niveau_id = fields.Many2one('class.niveau', 'niveau',
                                required=True, help='Standard division')

    matiere_ids = fields.Many2many('matiere.matiere', 'matiere_standards_rel',
                                   'class_id','matiere_id',  'Subject',
                                   help='Subjects of the standard')
    user_id = fields.Many2one('teacher.teacher', 'Class Teacher',
                              help='Teacher of the standard')
    student_ids = fields.One2many('student.student', 'standard_id',
                                  'Student In Class',
                                  compute='_compute_student', store=True,
                                  help='Students which are in this standard'
                                  )
    color = fields.Integer('Color Index', help='Index of color')
    cmp_id = fields.Many2one('res.company', 'Company Name',
                             related='school_id.company_id', store=True,
                             help='Company_id of the school')

    total_no_matieres = fields.Integer('Total No of matieres',
                                       compute="_compute_matieres",
                                       help='Total matieres in class')
    name = fields.Char('Name', help='Standard name')
    capacity = fields.Integer("Total Seats", help='Standard capacity')
    total_students = fields.Integer("Total Students",
                                    compute="_compute_total_student",
                                    store=True,
                                    help='Total students of the standard')
    remaining_seats = fields.Integer("Available Seats",
                                     compute="_compute_remain_seats",
                                     store=True,
                                     help='Remaining seats of the standard')




    teacher_id = fields.Many2many('teacher.teacher',
                                  'teacher_classs_rel',
                                  'class_id', 'teacher_id',
                                  'tags', help='Select teachers')

    student_id = fields.One2many('student.student', 'class_name', string=" class")


    @api.onchange('speciality_id', 'niveau_id')
    def onchange_combine(self):
        self.name = str(self.speciality_id.name
                        ) + '-' + str(self.niveau_id.name)


    @api.constrains('speciality_id', 'niveau_id')
    def check_standard_unique(self):
        speciality_search = self.env['class.room'].search([
            ('speciality_id', '=', self.speciality_id.id),
            ('niveau_id', '=', self.niveau_id.id),
            ('school_id', '=', self.school_id.id),
            ('id', 'not in', self.ids)])
        if speciality_search:
            raise ValidationError(_("Division and class should be unique!"))


    def unlink(self):
        for rec in self:
            if rec.student_ids or rec.matiere_ids:
                raise ValidationError(_(
                    "You cannot delete as it has reference with student, subject or syllabus!"))
        return super(ClassRoom, self).unlink()


    @api.constrains('capacity')
    def check_seats(self):
        if self.capacity <= 0:
            raise ValidationError(_("Total seats should be greater than 0!"))


    def name_get(self):
        return [(rec.id, rec.speciality_id.name + '[' + rec.niveau_id.name +
                 ']') for rec in self]
