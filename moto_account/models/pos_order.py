# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _prepare_invoice_line(self, order_line):
        values = super(PosOrder, self)._prepare_invoice_line(order_line)
        if self.amount_total < 0.00 and values.get('tax_ids'):
            account = order_line.product_id and order_line.product_id.categ_id and order_line.product_id.categ_id.property_account_refund_categ_id
            if account:
                values.update({
                    'account_id': account.id,
                })
        return values
