# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ParentRelation(models.Model):
    '''Defining a Parent relation with child.'''

    _name = "parent.relation"
    _description = "Parent-child relation information"

    name = fields.Char("Relation name", required=True,
                       help='Parent relation with student')


class SchoolParent(models.Model):
    '''Defining a Teachrelationer information.'''

    _name = 'school.parent'
    _description = 'Parent Information'

    partner_id = fields.Many2one('res.partner', 'User ID', ondelete="cascade",
                                 delegate=True, required=True,
                                 help='Partner which is user over here')

    relation_id = fields.Many2one('parent.relation', 'Relation with Child',
                                                                     help='Parent relation with child')
    student_id = fields.Many2many('student.student', 'students_parents_rel',
                                  'students_parent_id', 'student_id',
                                  'Children',)

    teacher_id = fields.Many2one('teacher.teacher', 'Teacher',
                                store=True,
                                 help='Teacher of a student')


    image = fields.Binary('Photo', default=_default_image,
                              help='Attach student photo')



