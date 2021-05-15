{
    'name': 'GEC: Accounting',
    'summary':
        """
        Modulo que modifica tanto la forma en la que se muestran los diarios en los documentos,
        contabilidad analítica, y agrega campos en los tipos de facturas de proveedor y de clientes.
        """,
    'description':
        """
        Grupo Empresarial Camacho :\n
        1. Se modifica la visualización de diarios dependiendo del tipo de documento que se esté generando.\n
        2. Se agregan campos de validación en las facturas de proveedor para autorizar los pagos.\n
        3. Se crean campos de tipo de obligación para la creación de cuentas analíticas. Si se selecciona la opción de 
        obligación financiera, se mostrarán los nuevos campos agregados de tipo de crédito, plazos y cupo bancario,
        los cuales son obligatorios.\n
        4. Se agrega el campo de almacén en las facturas, el cual permite realizar el filtrado de los diarios correspondientes.\n
        5. Se agrega el campo almacén asociado a los diarios contables.\n
        5. Se crean los consecutivos para las cotizaciones por cada almacén.\n
        
    
        """,
    'license': 'OEEL-1',
    'author': 'GECamacho (Nodier Vasquez)',
    'version': '1.0',
    "category": "Extra Tools",
    'depends': ['account','account_accountant','stock','sale','purchase'],
    'data': [
        'views/account_move_view.xml',
        'views/analytic_account_view.xml',
        'views/account_journal_view.xml',
        'views/sale_order_sequences.xml',
        'views/purchase_order_sequences.xml',

    ],
    'installable': True,

    #     "license": "AGPL-3",

}