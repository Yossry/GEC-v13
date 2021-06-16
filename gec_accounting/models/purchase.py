from odoo import api, fields, models, _
from odoo.exceptions import UserError
import re


class PurchaseOrderWarehouse(models.Model):
    _inherit = 'purchase.order'

    name = fields.Char('Order Reference', required=True, index=True,
                       copy=False, default='New')

    partner_ref = fields.Char(size=15)

    @api.model
    def create(self, vals):
        bg = self.env['stock.picking.type'].browse(vals.get('picking_type_id'))
        wh = self.env['stock.warehouse'].browse(bg.warehouse_id.id)
        p = 'p'
        if vals.get('name', 'New') == 'New':
            if wh.code in ('HCALL', 'H52', 'H33', 'HD52', 'HDBQ', 'HSA', 'HSM', 'AKT'):
                vals['name'] = self.env['ir.sequence'].next_by_code('%s%s' %(wh.code.lower(), p))
        res = super(PurchaseOrderWarehouse, self).create(vals)
        return res

    @api.onchange('partner_ref')
    def partner_ref_onchange(self):
        self.partner_ref = re.sub(r'([.!"#$%&()?+=,;*:/ ])', '',
                                  self.partner_ref.upper()) \
            if self.partner_ref else self.partner_ref

