# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning

class ResUsers(models.Model):
    _inherit = 'res.users'

    restrict_locations = fields.Boolean('Restrict Location')

    # warehouse_id = fields.Many2many('stock.warehouse', string='Almacén',
    #                                help='Seleccione el/los almecén/es a los que tiene acceso el usuario.')

    stock_location_ids = fields.Many2many(
        'stock.location',
        'location_security_stock_location_users',
        'user_id',
        'location_id',
        'Stock Locations')

    default_picking_type_ids = fields.Many2many(
        'stock.picking.type', 'stock_picking_type_users_rel',
        'user_id', 'picking_type_id', string='Default Warehouse Operations',)


class stock_move(models.Model):
    _inherit = 'stock.move'

    @api.constrains('state', 'location_id', 'location_dest_id')
    def check_user_location_rights(self):
        for rec in self:
            if rec.state == 'draft':
                return True

            user_locations = rec.env.user.stock_location_ids
            if rec.env.user.restrict_locations:
                message = _(
                    'Invalid Location. You cannot process this move since you do '
                    'not control the location "%s". '
                    'Please contact your Adminstrator.')
                if rec.location_id not in user_locations:
                    raise Warning(message % rec.location_id.name)
                elif rec.location_dest_id not in user_locations:
                    raise Warning(message % rec.location_dest_id.name)