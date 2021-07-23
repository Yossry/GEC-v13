# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import exceptions
from odoo.addons.sale.controllers.portal import CustomerPortal
from odoo.http import request, route
from odoo.tools import consteq


class JournalItems(CustomerPortal):

    def _journal_items_by_partner(self, account, partner, access_token=None):
        result = request.env['account.move.line'].browse([account, partner])
        result_sudo = result.sudo()
        try:
            result.check_access_rights('read')
            result.check_access_rule('read')
        except exceptions.AccessError:
            if not access_token or not consteq(result_sudo.sale_id.access_token, access_token):
                raise
        return result_sudo

