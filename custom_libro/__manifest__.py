# -*- coding: utf-8 -*-
{
    'name': "custom_libro",

    'summary': """
        Modulo de selección de diarios contables""",

    'description': """
        Modulo para seleccionar los diarios contables para facturas recepciones y pagos de cliente, tanto de clientes como de proveedores.
    """,

    'author': "Nodier Vasquez - OdooGEC,
    #'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account.move.py'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'views/views.xml',
    ],
    
}
