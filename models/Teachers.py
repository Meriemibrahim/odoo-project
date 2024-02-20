from odoo import api, fields, models


class SchoolTeacher(models.Model):
    _name = 'teacher.teacher'
    _description = 'Teacher Information'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    employee_id = fields.Many2one('hr.employee', 'Employee ID',
                                  ondelete="cascade",
                                  delegate=True, required=True,
                                  help='Enter related employee')
    #
    category_ids = fields.Many2many('hr.employee.category',
                                    'teacher_category_rel', 'emp_id',
                                    'categ_id', 'Tags',
                                    help='Select employee category')
    department_id = fields.Many2one('hr.department', 'Department',
                                    help='Select department')
    matiere_ids = fields.Many2one("matiere.matiere", "matieres", help='Select matiere')
    phone_numbers = fields.Char("Phone Number", help='Student PH no')
    class_id = fields.Many2many('class.room', 'class_teacher_relation', 'class_id', 'teacher_id',
                                help='Select class')

    image = fields.Binary('Photo',
                          help='Attach student photo')
    is_parent = fields.Boolean('Is Parent',
                               help='Select this if it parent')
    stu_parent_id = fields.Many2one('school.parent', 'Related Parent',
                                    help='Enter student parent')
    student_id = fields.Many2many('student.student',
                                  'students_teachers_parent_rel',
                                  'teacher_id', 'student_id',
                                  'Children', help='Select student')
