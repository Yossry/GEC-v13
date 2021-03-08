# -*- coding: utf-8 -*-
 from odoo import models, fields, api


 class custom_libro(models.Model):
    _inherit = 'account.journal'
    
    libro = field.Many2one('account.journal', string='Libro', required=True, readonly=True,
        states={'draft': [('readonly', False)]}, domain="[('company_id', '=', company_id)]",
        default=_get_default_journal)
    
        
