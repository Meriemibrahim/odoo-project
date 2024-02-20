import base64
from odoo import fields, api, models
from odoo.exceptions import UserError, ValidationError
from odoo.modules import get_module_resource


class StudentStudent(models.Model):
    _name = 'student.student'
    _description = 'Students'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin']


    @api.depends('date_of_birth')
    def _compute_student_age(self):
        current_dt = fields.Date.today()
        for rec in self:
            rec.age = 0
            if rec.date_of_birth and rec.date_of_birth < current_dt:
                start = rec.date_of_birth
                age_calc = ((current_dt - start).days / 365)
                # Age should be greater than 0
                if age_calc > 0.0:
                    rec.age = age_calc

    name = fields.Char("Name")
    middle = fields.Char('Middle Name', required=True, )
    class_name = fields.Many2one("class.room", string="class name", )
    # class_id = fields.One2many("class.room", "student_id", string="student's name", )
    active = fields.Boolean("Active")
    # emergency_phone = fields.Char('Emergency_phone', store=True)
    # mobile_phone = fields.Char('phone Mobile')
    email = fields.Char('Email')
    notes = fields.Text('Notes')
    color = fields.Integer('Color Index', default=0)
    # barcode = fields.Char(string="Badge ID", help="ID used for employee identification.",
    #                       copy=False)
    parent_id = fields.Many2many('school.parent', 'students_parents_rel',
                                 'student_id',
                                 'students_parent_id', 'Parent(s)',
                                 help='Enter student parents')
    # family_con_ids = fields.One2many('student.family.contact',
    #                                  'family_contact_id',
    #                                  'Family Contact Detail',
    #                                  help='Select the student family contact')
    standard_id = fields.Many2one('student.student','standard')
    user_id = fields.Many2one('res.users', 'User ID', ondelete="cascade",
                              required=True, delegate=True,
                              help='Select related user of the student')
    student_name = fields.Char('Student Name',
                               store=True,)
    contact_phone = fields.Char('Phone no.', help='Enter student phone no.')
    contact_mobile = fields.Char('Mobile no', help='Enter student mobile no.')
    roll_no = fields.Integer('Roll No.', readonly=True,
                             help='Enter student roll no.')

    @api.model
    def _default_image(self):
        image_path = get_module_resource('gestion_ecole', 'static/src/img',
                                         'index.png')
        return base64.b64encode(open(image_path, 'rb').read())

    photo = fields.Binary('Photo', default=_default_image,
                          help='Attach student photo')


    year = fields.Many2one('academic.year', 'Academic Year',
                           help='Select academic year')
    # relation = fields.Many2one('student.relation.master', 'Relation',
    #                            help='Select student relation')

    admission_date = fields.Date('Admission Date', default=fields.Date.today(),
                                 help='Enter student admission date')
    last = fields.Char('Surname', required=True,

                       help='Enter student last name')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],
                              'Gender',
                              help='Select student gender')
    date_of_birth = fields.Date('BirthDate', required=True,

                                help='Enter student date of birth')
    age = fields.Integer(compute='_compute_student_age', string='Age',
                         readonly=True, help='Enter student age')

    @api.depends('date_of_birth')
    def _compute_student_age(self):
        current_dt = fields.Date.today()
        for rec in self:
            rec.age = 0
            if rec.date_of_birth and rec.date_of_birth < current_dt:
                start = rec.date_of_birth
                age_calc = ((current_dt - start).days / 365)
                # Age should be greater than 0
                if age_calc > 0.0:
                    rec.age = age_calc
    maritual_status = fields.Selection([('unmarried', 'Unmarried'),
                                        ('married', 'Married')],
                                       'Marital Status',

                                       help='Select student maritual status')

    doctor = fields.Char('Doctor Name',
                         help='Enter doctor name for student medical details')
    designation = fields.Char('Designation', help='Enter doctor designation')
    doctor_phone = fields.Char('Contact No.', help='Enter doctor phone')
    blood_group = fields.Char('Blood Group', help='Enter student blood group')
    height = fields.Float('Height', help="Hieght in C.M")
    weight = fields.Float('Weight', help="Weight in K.G")
    eye = fields.Boolean('Eyes', help='Eye for medical info')
    ear = fields.Boolean('Ears', help='Eye for medical info')
    nose_throat = fields.Boolean('Nose & Throat',
                                 help='Nose & Throat for medical info')
    respiratory = fields.Boolean('Respiratory',
                                 help='Respiratory for medical info')
    cardiovascular = fields.Boolean('Cardiovascular',
                                    help='Cardiovascular for medical info')
    neurological = fields.Boolean('Neurological',
                                  help='Neurological for medical info')
    muskoskeletal = fields.Boolean('Musculoskeletal',
                                   help='Musculoskeletal for medical info')
    dermatological = fields.Boolean('Dermatological',
                                    help='Dermatological for medical info')
    blood_pressure = fields.Boolean('Blood Pressure',
                                    help='Blood pressure for medical info')
    comment = fields.Text('comment',
                          help='comment about medical')
    remark = fields.Text('Remark',
                         help='remark')
    school_id = fields.Many2one('school.school', 'School',

                                help='Select school')


    certificate_ids = fields.One2many('student.certificate', 'student_id',
                                      'Certificate',)

    document = fields.One2many('student.document', 'doc_id', 'Documents',
                               help='Attach student documents')
    description = fields.One2many('student.description', 'des_id',
                                  'Description', help='Description')
    prix_list = fields.One2many('prix.prix', 'prix_list_id',
                                 'prix List', help='Student prix list')

    academic_year = fields.Char('Year', related='year.name',
                                help='Academic Year', )

    active = fields.Boolean(default=True,
                            help='Activate/Deactivate student record')



