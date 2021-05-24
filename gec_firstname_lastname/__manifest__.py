{
    'name': 'GECamacho: Custom contacts',    
    'summary':
    """
    Modificación del modulo de contactos.
    """,
    'description': 
    """
    Grupo Empresarial Camacho - Modulo de contactos:\n
    1. Se agregan los campos de nombres y apellidos divididos.\n
    2. Los nombre y apellidos se cambian a mayúscula.\n
    3. Se Oculta el campo nombre cuando se crea un contacto individual y se obliga a escribir nombres y apellidos.\n
    4. Se deja por defectos los valores de Cédula de ciudadanía y NIT, para contacto individual o compañía respectivamente.\n
    5. Se agrega un campo llamado documentos en el que se agregará la ducmentación correspondiente al contacto.\n
    6. En la vista de arbol se agregan los campos de numero de documento, primer nombre, segundo nombre, primer apellido y segundo apellido. \n
    7. Se validan que los números de documentos ingresados correspondan al tipo de documento.\n
    
    """,
    'license': 'OEEL-1',
    'author': 'GE-Camacho',
    'version': '2.0',
    "category": "Extra Tools",
    'depends': ['base'],
    'data': [
        'views/res_partner_view.xml',
      
    ],
    'installable': True,    
    
#     "license": "AGPL-3",
    
    
}