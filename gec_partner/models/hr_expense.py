from odoo import api, fields, models


class Expenses(models.Model):
    _inherit = 'hr.expense'


    employee_id = fields.Many2one('res.partner', string="Asociado",
                                  required=True, readonly=True,
                                  states={'draft': [('readonly', False)],
                                          'reported': [('readonly', False)],
                                          'refused': [('readonly', False)]},
                                  check_company=True)