from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    operation_type = fields.Selection([('terceros', 'Terceros'), (
    'obli_financiera', 'Obligación Financiera')], default='terceros',
                                      string='Tipo de operación')

    credit_type = fields.Selection(
        [('ordinario', 'Ordinario'), ('ordinario_lp', 'Ordinario Largo Plazo'),
         ('credi_express', 'CrediExpress'), ('virtual', 'Virtual'),
         ('tesoreria', 'Tesoreria'), ('leasing', 'Leasing'),
         ('factoring', 'Factoring')], string='Tipo de crédito')

    term = fields.Integer(string='Plazos')

    credit_rate = fields.Integer(string='Tasa')

    bank_quote = fields.Monetary(string='Cupo Bancario')

    # total_payed = fields.Monetary(compute='_payed_total', string="Total Payed",
    #                               groups='account.group_account_invoice')

    @api.model
    def create(self, vals):
        res = super(AnalyticAccount, self).create(vals)

        if res.operation_type == 'obli_financiera':
            if res.term <= 0 or res.term > 130:
                raise UserError(
                    '¡Los plazos de pago deben estar entre 1 y 130 meses!')
            if res.bank_quote <= 0:
                raise UserError(
                    'El cupo bancario no puede ser inferior o igual a cero.')

        return res

    def write(self, vals):
        res = super(AnalyticAccount, self).write(vals)
        if vals.get('operation_type') == 'obli_financiera':
            if self.term <= 0 or self.term > 130:
                raise UserError(
                    '¡Los plazos de pago deben estar entre 1 y 130 meses!')
            if self.bank_quote <= 0:
                raise UserError(
                    'El cupo bancario no puede ser inferior o igual a cero.')

        return res

    @api.onchange('name', 'operation_type', 'credit_type')
    def oper_type_onchange(self):

        if self.name:
            if self.operation_type:
                if self.operation_type == 'terceros':
                    self.code = self.name.upper()
                    self.credit_type = ''
                    self.term = ''
                    self.bank_quote = ''

        if self.operation_type == 'obli_financiera':
            if self.credit_type:
                self.code = self.credit_type.upper()

    @api.onchange('name')
    def name_onchange(self):

        if self.name:
            self.name = self.name.upper()
        else:
            pass

    # def _payed_total(self):
    #     account_invoice_report = self.env['account.invoice.report']
    #     if not self.ids:
    #         return True
    #
    #     user_currency_id = self.env.company.currency_id.id
    #     all_partners_and_children = {}
    #     all_partner_ids = []
    #     for partner in self:
    #         # price_total is in the company currency
    #         all_partners_and_children[partner] = self.with_context(
    #             active_test=False).search([('id', 'child_of', partner.id)]).ids
    #         all_partner_ids += all_partners_and_children[partner]
    #
    #     # searching account.invoice.report via the ORM is comparatively expensive
    #     # (generates queries "id in []" forcing to build the full table).
    #     # In simple cases where all invoices are in the same currency than the user's company
    #     # access directly these elements
    #
    #     # generate where clause to include multicompany rules
    #     where_query = account_invoice_report._where_calc([
    #         ('partner_id', 'in', all_partner_ids),
    #         ('state', 'not in', ['draft', 'cancel']),
    #         ('type', 'in', ('out_invoice', 'out_refund'))
    #     ])
    #     account_invoice_report._apply_ir_rules(where_query, 'read')
    #     from_clause, where_clause, where_clause_params = where_query.get_sql()
    #
    #     # price_total is in the company currency
    #     query = """
    #               SELECT SUM(price_subtotal) as total, partner_id
    #                 FROM account_invoice_report account_invoice_report
    #                WHERE %s
    #                GROUP BY partner_id
    #             """ % where_clause
    #     self.env.cr.execute(query, where_clause_params)
    #     price_totals = self.env.cr.dictfetchall()
    #     for partner, child_ids in all_partners_and_children.items():
    #         partner.total_invoiced = sum(
    #             price['total'] for price in price_totals if
    #             price['partner_id'] in child_ids)