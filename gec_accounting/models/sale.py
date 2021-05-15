from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrderWarehouse(models.Model):
    _inherit = "sale.order"

    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse',
                                   domain="[('company_id', '=', company_id)]")

    name = fields.Char(string='Order Reference', required=True, copy=False,
                       readonly=True, states={'draft': [('readonly', False)]},
                       index=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        wh = self.env['stock.warehouse'].browse(vals.get('warehouse_id'))
        if vals.get('name', _('New')) == _('New'):
            # if wh.code == 'KENND':
            #     vals['name'] = self.env['ir.sequence'].next_by_code(wh.code.lower())
            # elif wh.code == 'CHAPI':
            #     vals['name'] = self.env['ir.sequence'].next_by_code(wh.code.lower())
            # elif wh.code == 'HCALL':
            if wh.code == 'HCALL':
                vals['name'] = self.env['ir.sequence'].next_by_code(wh.code.lower())
            elif wh.code == 'H52':
                vals['name'] = self.env['ir.sequence'].next_by_code(wh.code.lower())
            elif wh.code == 'H33':
                vals['name'] = self.env['ir.sequence'].next_by_code(wh.code.lower())
            elif wh.code == 'HD52':
                vals['name'] = self.env['ir.sequence'].next_by_code(wh.code.lower())
            elif wh.code == 'HDBQ':
                vals['name'] = self.env['ir.sequence'].next_by_code(wh.code.lower())
        res = super(SaleOrderWarehouse, self).create(vals)
        return res


    @api.model
    def _prepare_invoice(self):

        res = super(SaleOrderWarehouse, self)._prepare_invoice()
        res['warehouse_id'] = self.warehouse_id.id

        return res

    def _create_invoices(self, grouped=False, final=False):
        res = super(SaleOrderWarehouse, self)._create_invoices()

        res['journal_id'] = res.journal_id.search(
            [('warehouse_id', '=', self.warehouse_id.name),
             ('type', '=', 'sale')], limit=1)

        print(res)

        return res


#
