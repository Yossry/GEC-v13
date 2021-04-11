from odoo import api, fields, models
from odoo.exceptions import UserError
import re


class ResPartner(models.Model):
    _inherit = 'res.partner'

    fname = fields.Char(string='Primer Nombre')
    sname = fields.Char(string='Segundo Nombre')
    flastname = fields.Char(string='Primer Apellido')
    slastname = fields.Char(string='Segundo Apellido')

    # @api.model
    # def create(self, vals):
    #     res = super(ResPartner, self).create(vals)
    #     return res
    #
    # def write(self, vals):
    #     res = super(ResPartner, self).write(vals)
    #     return res

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
