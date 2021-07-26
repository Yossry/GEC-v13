{
    'name': 'GEC: Pos Product Ref',
    'summary':
        """
        Se agrega referencia en POS
        """,
    'description':
        """
        
        Grupo Empresarial Camacho:
        
        1. Se agregan el campo de referencia en la ficha de producto de POS.\n
    
        """,
    'license': 'OEEL-1',
    'author': 'Nodier Vasquez - (GE-Camacho)',
    'version': '13.0',
    "category": "Extra Tools",
    'depends': ['point_of_sale', 'product'],
    'data': [
        'views/assets.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,

}
