# -*- coding: utf-8 -*-
from odoo import models, fields, api


class custom_libro(models.Model):
    _inherit = 'account.move'
    
    #libro = fields.Char(string='Diario Contable')
    
    # CLIENTES FACTURAS (VENTAS)
    #libro = fields.Many2one('account.journal', string='Diario Cont', domain="['&',['company_id', '=', company_id],['type','=','sale']]")
    
    #company_id = self._context.get('force_company', self._context.get('default_company_id', self.env.company.id))
    
    # PROVEEDOR FACTURAS (COMPRAS)
    #libro = fields.Many2one('account.journal', string='Diario Cont', domain="['&',['company_id', '=', company_id],['type','=','purchase']]")
    
    #raise Warning ("Que tipo de documento es?: ")
    # PAGOS (BANCOS - EFECTIVO)
    libro = fields.Many2one('account.journal', string='Diario Cont', domain="['&',['company_id', '=', company_id], '|',['type','=','cash'],['type','=','bank']]")
    
    tipo = fields.Char(string='Tipo')
    
    # RECEPCIONES (VARIOS - BANCOS - EFECTIVO)
    #libro = fields.Many2one('account.journal', string='Diario Cont', domain="['&',['company_id', '=', company_id], '|','|',['type','=','general'],['type','=','bank'],['type','=','cash']]")

    #@api.model 
    #def _move_type(self):
    #    move_type = self._context.get('default_type', 'entry')
    
    