# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, Warning
from odoo.addons import decimal_precision as dp
from odoo.tools import float_compare, float_round


class ProductCategory(models.Model):
    _inherit = 'product.category'

    property_account_refund_categ_id = fields.Many2one('account.account', company_dependent=True,
                                                       string="Refund Account",
                                                       domain="['&', ('deprecated', '=', False), ('company_id', '=', current_company_id)]",
                                                       help="This account will be used when issuing credit notes.")
