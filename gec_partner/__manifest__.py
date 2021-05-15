{
    'name': 'GEC: Partner',
    'summary':
    """
    Modificación del modulo de contactos.
    """,
    'description': 
    """
    
    Grupo Empresarial Camacho - Modulo de contactos:
    
    1. Se agregan los campos de nombres y apellidos divididos.\n
    2. Los nombre y apellidos se cambian a mayúscula automáticamente.\n
    3. Se Oculta el campo nombre cuando se crea un contacto individual y se obliga a escribir nombres y apellidos.\n
    4. Se deja por defectos los valores de Cédula de ciudadanía y NIT, para contacto individual o compañía respectivamente.\n
    5. Se agrega un campo llamado documentos en el que se agregará la ducmentación correspondiente al contacto.\n
    6. En la vista de arbol se agregan los campos de numero de documento, primer nombre, segundo nombre, primer apellido y segundo apellido. \n
    7. Se validan que los números de documentos ingresados correspondan al tipo de documento.\n
    8. Se bloquea la modificación de los contactos una vez tenga apuntes contables en el sistema. Se permitirá la modificación si es aprobado por el departamento encargado y queda la trazabilidad de quien la modificación y quién la realizó, para tener trazabilidad.\n
    
    
    """,
    'license': 'OEEL-1',
    'author': 'GECamacho',
    'version': '1.0',
    "category": "Extra Tools",
    'images': ['static/description/grupo_camacho.jpg'],
    'depends': ['base','account','hr_expense'],
    'data': [
        'views/res_partner_view.xml',
        # 'views/hr_expense_view.xml'

    ],
    'installable': True,    
    
#     "license": "AGPL-3",
    
    
}