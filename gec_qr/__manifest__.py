# -*- coding: utf-8 -*-
{
    'name': "gec_qr",

    'summary': """
        Se agregan elementos en base a la respuesta de de Carvajal en cuanto a la facturación electrónica.
        """,

    'description': """
        1. Se agrega el código QR que se genera a partir de la información entregada en el XML de la DIAN.
    """,

    'author': "GECamacho",
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['account','account_accountant','l10n_co_edi','l10n_co_edi_ubl_2_1'],

    'data': [
        'views/account_move_view.xml'
    ],
}
