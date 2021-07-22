from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = 'account.move.line'

    total_field = fields.Char('Campo de prueba')
    virtual_debe = fields.Char('Debe')
    virtual_haber = fields.Char('Haber')
    virtual_balance = fields.Char('Balance')

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
            tx = 'Debe: ' + "{:.2f}".format(debit) + \
                 ', Haber: ' + "{:.2f}".format(credit)+ \
                 ', Balance: '+ "{:.2f}".format(total)

            self.virtual_debe = "{:,.2f}".format(debit)
            self.virtual_haber = "{:,.2f}".format(credit)
            self.virtual_balance = "{:,.2f}".format(total)

            self.total_field = tx
            # raise UserError(tx)

    def partner_balances(self):
        return {
            'name': 'My Window',
            'domain': [],
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'context': {},
            'target': 'new',
        }