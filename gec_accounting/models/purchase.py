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
        if vals.get('name', 'New') == 'New':
            if wh.code == 'HCALL':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    wh.code.lower())
            elif wh.code == 'H52':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    wh.code.lower())
            elif wh.code == 'H33':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    wh.code.lower())
            elif wh.code == 'HD52':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    wh.code.lower())
            elif wh.code == 'HDBQ':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    wh.code.lower())
            elif wh.code == 'HSA':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    wh.code.lower())
            elif wh.code == 'HSM':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    wh.code.lower())
            elif wh.code == 'AKT':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    wh.code.lower())
        res = super(PurchaseOrderWarehouse, self).create(vals)
        print(res)
        return res

    @api.onchange('partner_ref')
    def partner_ref_onchange(self):
        self.partner_ref = re.sub(r'([.!"#$%&()?+=,;*:/ ])','',self.partner_ref.upper()) \
            if self.partner_ref else self.partner_ref
