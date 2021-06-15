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
        company_id = vals.get('company_id',
                              self.default_get(['company_id'])['company_id'])
        if vals.get('name', 'New') == 'New':
            seq_date = None
            if 'date_order' in vals:
                seq_date = fields.Datetime.context_timestamp(self,
                                                             fields.Datetime.to_datetime(
                                                                 vals[
                                                                     'date_order']))
            vals['name'] = self.env['ir.sequence'].with_context(
                force_company=company_id).next_by_code('purchase.order',
                                                       sequence_date=seq_date) or '/'
        return super(PurchaseOrder,
                     self.with_context(company_id=company_id)).create(vals)

    @api.model
    def create(self, vals):
        bg = self.env['stock.picking.type'].browse(vals.get('picking_type_id'))
        wh = self.env['stock.warehouse'].browse(bg.warehouse_id.id)
        p = 'p'
        if vals.get('name', 'New') == 'New':
            if self.company_id.id == 2:
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    '%s%s' % (wh.code.lower(), p))
        res = super(PurchaseOrderWarehouse, self).create(vals)
        print(res)
        return res

    @api.onchange('partner_ref')
    def partner_ref_onchange(self):
        self.partner_ref = re.sub(r'([.!"#$%&()?+=,;*:/ ])', '',
                                  self.partner_ref.upper()) \
            if self.partner_ref else self.partner_ref

    @api.model
    def create(self, vals):
        if self.company_id and vals.get('name', '/') == '/':
            if self.company_id.name == "YourFirstCompanyName":  # Company1
                seq_id = self.pool.get('ir.model.data').get_object_reference(
                        self._cr,
                        self._uid,
                        'sale_order',
                        'YourCompany1SequenceID')[
                        1]
                self.id = self.pool.get('ir.sequence').get_id(self._cr,
                                                              self._uid,
                                                              seq_id, 'id',
                                                              self._context)
                self.name = self.id

            if self.company_id.name == "YourSecondCompanyName":  # Company2
                seq_id = \
                    self.pool.get('ir.model.data').get_object_reference(
                        self._cr,
                        self._uid,
                        'sale_order',
                        'YourCompany2SequenceID')[
                        1]
                self.name = self.pool.get('ir.sequence').get_id(self._cr,
                                                                self._uid,
                                                                seq_id, 'id',
                                                                self._context)

            if self.company_id.name == "YourThirdCompanyName":  # Company3
                seq_id = \
                    self.pool.get('ir.model.data').get_object_reference(
                        self._cr,
                        self._uid,
                        'sale_order',
                        'YourCompany3SequenceID')[
                        1]
                self.name = self.pool.get('ir.sequence').get_id(self._cr,
                                                                self._uid,
                                                                seq_id, 'id',
                                                                self._context)
        return super(sale_order, self).create(vals)
