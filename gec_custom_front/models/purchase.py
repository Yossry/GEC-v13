from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order.line'

    test = fields.Char(string='Test field')
