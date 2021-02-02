# -*- coding: utf-8 -*-
{
    'name': "aag_pph21",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'hr_contract', 'hr_payroll_community','aag_add_field'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/structure_xacti.xml',
        'views/views.xml',
        'views/templates.xml',
	'views/view_ptkp.xml',
        'views/master_ptkp.xml',
        'views/views_pkp.xml',
        'views/master_pkp.xml',
        'views/employee.xml',
        'views/company.xml',
    #    'views/views_accpph21.xml',
        'views/payslip.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}