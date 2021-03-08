# -*- coding: utf-8 -*-
from odoo import models, fields, api


class custom_libro(models.Model):
    _inherit = 'account.move'
    
    libro = fields.Char(string='Diario Contable')
    
   