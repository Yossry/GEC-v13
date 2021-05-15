from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PurchaseOrderWarehouse(models.Model):
    _inherit = 'purchase.order'

    name = fields.Char('Order Reference', required=True, index=True,
                       copy=False, default='New')

    @api.model
    def create(self, vals):
        bg = self.env['stock.picking.type'].browse(vals.get('picking_type_id'))
        wh = self.env['stock.warehouse'].browse(bg.warehouse_id.id)
        if vals.get('name', 'New') == 'New':
            # if wh.code == 'KENND':
            #     vals['name'] = self.env['ir.sequence'].next_by_code(wh.code.lower())
            # elif wh.code == 'CHAPI':
            #     vals['name'] = self.env['ir.sequence'].next_by_code(wh.code.lower())
            # elif wh.code  == 'HCALL':
            if wh.code  == 'HCALL':
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
        res = super(PurchaseOrderWarehouse, self).create(vals)
        print(res)
        return res
