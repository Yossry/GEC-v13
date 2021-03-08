# -*- coding: utf-8 -*-
from odoo import models, fields, api


class custom_libro(models.Model):
    _name = 'diario'
    _inherit = 'account.journal'
    
    libro = fields.Char()
    
   