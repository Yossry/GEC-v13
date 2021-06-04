from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    warehouse_id = fields.Many2one('stock.warehouse', 'Almacén',
                                   ondelete='set null', index=True,
                                   tracking=True, store=True)

    journal_id = fields.Many2one('account.journal', string='Journal',
                                 readonly=True,
                                 states={'draft': [('readonly', False)]},
                                 domain="[('company_id', '=', company_id)]",
                                 default='')

    validate_treasurer = fields.Boolean(string="Validar")
    validate_treasurer_name = fields.Char(compute='_compute_treasurer_validator',
                               default='Por Validar', readonly=True,
                               store=True,
                               string='Validadación tesorería',
                               tracking=True)

    validate_accounting = fields.Boolean(string ="Validar")
    validate_accounting_name = fields.Char(compute='_compute_accounting_validator',
                                default='Por Validar', readonly=True,
                                store=True,
                                string='Validación contabilidad',
                                tracking=True)

    invoice_outstanding_credits_debits_widget = fields.Text(tracking=True)
    invoice_date = fields.Date(tracking=True)
    date = fields.Date(tracking=True)
    invoice_date_due = fields.Date(tracking=True)

    @api.depends('validate_treasurer')
    def _compute_treasurer_validator(self):
        for rec in self:
            rec.ensure_one()
            if rec.validate_treasurer:
                rec.validate_treasurer_name = self.env.user.name

    @api.depends('validate_accounting')
    def _compute_accounting_validator(self):
        for rec in self:
            rec.ensure_one()
            if rec.validate_accounting:
                rec.validate_accounting_name = self.env.user.name

    def write(self, vals):
        res = super(AccountMove, self).write(vals)

        return res

    @api.onchange('purchase_vendor_bill_id', 'purchase_id')
    def _onchange_purchase_auto_complete(self):

        if self.purchase_vendor_bill_id.purchase_order_id or self.purchase_id:
            warehouse = self.purchase_id.picking_type_id.warehouse_id
            if warehouse:
                self.warehouse_id = warehouse

        return super()._onchange_purchase_auto_complete()

    @api.onchange('type', 'warehouse_id')
    def _select_journal(self):

        if self.type == 'entry':  # Entrada de diario

            self.journal_id = self.journal_id.search(
                [('warehouse_id', '=', self.warehouse_id.name)], limit=1)

            return {'domain': {
                'journal_id': [('warehouse_id', '=', self.warehouse_id.name)]}}

        elif self.type == 'out_invoice' or self.type == 'out_refund':  # Factura cliente o Nota credito cliente

            self.journal_id = self.journal_id.search(
                [('warehouse_id', '=', self.warehouse_id.name),
                 ('type', '=', 'sale')], limit=1)

            return {'domain': {'journal_id': [('type', '=', 'sale'), (
                'warehouse_id', "=", self.warehouse_id.name)]}}

        elif self.type == 'in_invoice' or self.type == 'in_refund':  # Factura proveedor proveedor o Nota credito proveedor

            self.journal_id = self.journal_id.search(
                [('warehouse_id', '=', self.warehouse_id.name),
                 ('type', '=', 'purchase')], limit=1)

            return {'domain': {'journal_id': [('type', '=', 'purchase'), (
                'warehouse_id', '=', self.warehouse_id.name)]}}

        elif self.type == 'out_receipt' or self.type == 'in_receipt':  # Recibo de ventas o recibo de compras

            self.journal_id = self.journal_id.search(
                [('warehouse_id', '=', self.warehouse_id.name),
                 ('type', 'not in', ['sale', 'purchase'])], limit=1)

            return {
                'domain': {'journal_id': [
                    ('warehouse_id', '=', self.warehouse_id.name),
                    ('type', 'not like', 'sale'), (
                        'type', 'not like', 'purchase')]}}
