from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    warehouse_id = fields.Many2one('stock.warehouse', string='Almacén asociado')

