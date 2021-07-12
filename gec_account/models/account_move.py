from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


class AccountMove(models.Model):
    _inherit = 'account.move.line'

    test_field = fields.Char('Campo de prueba')

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

            self.test_field = tx
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