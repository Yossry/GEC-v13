from odoo import api, fields, models
from odoo.exceptions import UserError
import re


class ResPartner(models.Model):
    _inherit = 'res.partner'

    name = fields.Char(tracking=True)
    # l10n_co_document_type = fields.Selection(tracking=True)
    # l10n_co_document_type = fields.Selection([('rut', 'NIT'),
    #                                           ('id_card',
    #                                            'Tarjeta de Identidad'),
    #                                           ('passport', 'Pasaporte'),
    #                                           ('foreign_id_card',
    #                                            'Cédula Extranjera'),
    #                                           ('national_citizen_id',
    #                                            'Cédula de ciudadanía')],
    #                                          string='Document Type',
    #                                          help='Doc test',
    #                                          tracking=True)
    vat = fields.Char(tracking=True)

    fname = fields.Char(string='Primer Nombre')
    sname = fields.Char(string='Segundo Nombre')
    flastname = fields.Char(string='Primer Apellido')
    slastname = fields.Char(string='Segundo Apellido')
    edit_name = fields.Boolean(string='Editar', default=False, tracking=True,
                               help='Seleccionar si se autoriza la modificación del contacto, teniendo en cuenta que ya tiene apuntes contables.')
    account_move_count = fields.Integer(string='Apuntes Contables',
                                        compute='_compute_account_move_line_count')

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
        # if self.company_type == 'person':
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
    def doc_type_onchange(self):
        if self.company_type == 'person':
            if self.l10n_co_document_type == 'id_document' or self.l10n_co_document_type == 'rut':
                self.l10n_co_document_type = 'national_citizen_id'

        if self.company_type == 'company':
            self.l10n_co_document_type = 'rut'

class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    # @api.model
    # def _get_supported_account_types(self):
    #     return [('bank', _('Normal'))]

    acc_type = fields.Selection(selection=lambda x: x.env['res.partner.bank'].get_supported_account_types(), compute='_compute_acc_type', string='Type', help='Bank account type: Normal or IBAN. Inferred from the bank account number.')

