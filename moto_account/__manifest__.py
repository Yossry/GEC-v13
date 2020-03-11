# -*- coding: utf-8 -*-
{
    'name': 'MotoWorld: Account',
    'summary': 'MotoWorld: Phase 1B - Returns, Credit Notes and Invoice Sequences',
    'description':
    """
2199389
1. Add a new account field on (product.category) model
2. The system should not be able to validate invoices/credit notes/debit notes based on the document sequence number of the related journal
3. Set a specific restriction in the (account.invoice) model when a credit note is added to a customer invoice
    """,
    'license': 'OEEL-1',
    'author': 'Odoo Inc',
    'version': '0.2',
    'depends': ['account_accountant', 'l10n_co', 'l10n_co_edi', 'l10n_co_edi_ubl_2_1', 'l10n_co_reports'],
    'data': [
        'views/product_views.xml',
    ],
}
