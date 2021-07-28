{
    'name': 'GEC: Account Info',
    'summary':
        """
        Valor de asociado por cuentas.
        """,
    'description':
        """
    
        Grupo Empresarial Camacho:
    
        1. Se agrega campo informativo de valor por cada cuenta de un asociado.\n
        2. Se redirecciona a los apuntes contables filtrado por cada cuenta y asociado.\n
        
        """,
    'license': 'OEEL-1',
    'author': 'Nodier Vasquez (GE-Camacho)',
    'version': '1.0',
    "category": "Extra Tools",
    'depends': ['account','account_accountant'],
    'data': [
        'views/account_move_views.xml',
        'views/assets.xml',
    ],
    'qweb': ['static/src/xml/journal_items.xml'],
    'installable': True,


}
