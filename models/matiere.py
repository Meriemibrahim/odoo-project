from odoo import api, fields, models


class MatiereMatiere(models.Model):
    _name = 'matiere.matiere'
    _description = 'matiere Information'

    name = fields.Char('Name', required=True, help='matiere name')
    code = fields.Char('Code', required=True, help='matiere code')
    teachers_id = fields.Many2one('teacher.teacher',
                                   'teachers', help='Select teachers')
    department_id = fields.Many2one('hr.department', 'Department',
                                    help='Select department')





