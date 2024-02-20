# See LICENSE file for full copyright and licensing details.

{
    'name': 'School management',
    'version': '14.0.1.0.0',
    'author': '',
    'website': '',
    'category': 'School Management',
    'license': "AGPL-3",
    'complexity': 'easy',
    'Summary': 'A Module For School Management',
    'images': [],
    'depends': ['hr', 'crm', 'account', 'hr_recruitment', 'planning'],
    'data': [
        'security/secruity.xml',
        'security/ir.model.access.csv',
        'views/student_view.xml',

                 'views/parent_view.xml',

        'views/department_views.xml',
        'views/configuration.xml',
        'views/Teacher_views.xml',
        'views/classes.xml',
        'views/matiere.xml',
    ],
    'qweb': ["static/src/xml/dashboard.xml", ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': True,

}
