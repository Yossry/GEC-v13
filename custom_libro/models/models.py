# -*- coding: utf-8 -*-
from odoo import models, fields, api


class custom_libro(models.Model):
    _name = 'diario'
    _inherit = 'account.journal'
    
    libro = fields.Many2one('account.journal',widget='selection', domain="[('company_id', '=', company_id)]")
    
        
