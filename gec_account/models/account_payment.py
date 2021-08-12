from odoo import fields, models


class AccountPayments(models.Model):
    _inherit = 'account.payment'

    state = fields.Selection(tracking=True)

