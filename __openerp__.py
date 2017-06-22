# -*- coding: utf-8 -*-
{
    'name': "cash_management_approvals",

    'summary': """
        Cash Management Approvals Management""",

    'description': """
        Approvals Management extension for Cash Management
    """,

    'author': "dennokorir",
    'website': "http://www.tritel.co.ke",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'cash_management',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','tritel'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
