from odoo import api, fields, models, _


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    virtual_debe = fields.Char('Debe')
    virtual_haber = fields.Char('Haber')
    virtual_balance = fields.Char('Balance')
    show_widget = fields.Boolean('M_W')

    @api.onchange('account_id', 'partner_id')
    def validacion(self):
        debit = credit = 0
        if self.account_id and self.partner_id:
            for line in self.env['account.move.line'].search(
                    [('account_id', '=', self.account_id.code),
                     ('partner_id', '=', self.partner_id.name)]):

                if line.debit:
                    debit += line.debit
                elif line.credit:
                    credit += line.credit

            total = debit - credit

            self.virtual_debe = "{:,.2f}".format(debit)
            self.virtual_haber = "{:,.2f}".format(credit)
            self.virtual_balance = "{:,.2f}".format(total)

    def compute_show_balance(self):
        self.show_widget = False

class AccountMove(models.Model):
    _inherit = 'account.move'

    test_f = fields.Char('test')

    @api.onchange('type')
    def compute_show_balance(self):
        if self.type == 'entry':
            for line in self.line_ids:
                line.show_widget = True

