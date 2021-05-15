from odoo import api, fields, models
from odoo.exceptions import UserError
import re


class ResPartner(models.Model):
    _inherit = 'res.partner'

    name = fields.Char(tracking=True)
    l10n_co_document_type = fields.Selection(tracking=True)
    vat = fields.Char(tracking=True)

    fname = fields.Char(string='Primer Nombre')
    sname = fields.Char(string='Segundo Nombre')
    flastname = fields.Char(string='Primer Apellido')
    slastname = fields.Char(string='Segundo Apellido')
    edit_name = fields.Boolean(string='Editar', default=False, tracking=True)
    account_move_count = fields.Integer(string='Apuntes Contables', compute='_compute_account_move_line_count')

    @api.model
    def _compute_account_move_line_count(self):
        results = self.env['account.move.line'].read_group(
            [('partner_id', 'in', self.ids)], ['partner_id'], ['partner_id'])
        dic = {}
        for x in results: dic[x['partner_id'][0]] = x['partner_id_count']
        for record in self: record[
            'account_move_count'] = dic.get(record.id, 0)

    @api.model
    def create(self, vals):
        res = super(ResPartner, self).create(vals)
        return res

    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        return res

    @api.onchange('fname', 'sname', 'flastname', 'slastname')
    def name_onchange(self):
        if self.company_type == 'person' and self.fname and self.flastname:

            self.fname = self.fname.upper()
            self.flastname = self.flastname.upper()
            self.name = self.fname + ' ' + self.flastname

            if self.sname:
                self.sname = self.sname.upper()
                self.name = self.fname + ' ' + self.sname + ' ' \
                    + self.flastname

            if self.slastname:
                self.slastname = self.slastname.upper()
                self.name = self.fname + ' ' + self.flastname + ' ' + \
                    self.slastname

            if self.sname and self.slastname:
                self.name = self.fname + ' ' + self.sname + ' ' + \
                            self.flastname + ' ' + self.slastname

    @api.onchange('company_type', 'name')
    def company_onchange(self):
        if self.company_type == 'company':
            self.l10n_co_document_type = 'rut'
            if self.name:
                self.name = self.name.upper()
            self.fname = self.sname = self.flastname = self.slastname = ''
        if self.company_type == 'person':
            self.l10n_co_document_type = 'national_citizen_id'

    @api.onchange('vat')
    def vat_onchange(self):
        if self.company_type == 'person':
            if self.l10n_co_document_type != 'passport':
                self.vat = re.sub(r'([\D])', '', self.vat) if self.vat \
                    else self.vat
            else:
                self.vat = re.sub(r'([\W _])', '', self.vat) if self.vat \
                    else self.vat
        if self.company_type == 'company':
                self.vat = re.sub(r'([a-zA-Z.!"#$%&()+=,;*:/ ])', '',
                                  self.vat) if self.vat else self.vat

    @api.onchange('l10n_co_document_type')
    def vat_onchange(self):
        if self.l10n_co_document_type == 'id_document':
            raise UserError(
                'Por favor use la opción Cédula de ciudadanía para registrar '
                'un contacto con este tipo de documento.')


    # def action_view_account_analytic_line(self):
    #     """ return the action to see all the analytic lines of the project's analytic account """
    #     action = self.env.ref('analytic.account_analytic_line_action').read()[0]
    #     action['context'] = {'default_account_id': self.analytic_account_id.id}
    #     action['domain'] = [('account_id', '=', self.analytic_account_id.id)]
    #     return action



