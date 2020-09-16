# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, Warning
from odoo.addons import decimal_precision as dp
from odoo.tools import float_compare, float_round
from datetime import date


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    def _reverse_move_vals(self, default_values, cancel=True):
        # we want to pass in a different account for each move lines
        move_vals = super(AccountMove, self)._reverse_move_vals(default_values, cancel=cancel)
        if self.type == 'out_invoice':
            for line_command in move_vals.get('line_ids', []):
                line_vals = line_command[2]
                if line_vals.get('tax_ids'):
                    product_id = line_vals.get('product_id')
                    product = self.env['product.product'].browse(product_id)
                    account = product and product.categ_id and product.categ_id.property_account_refund_categ_id
                    if account:
                        line_vals.update({
                            'account_id': account.id,
                        })
        return move_vals

    def post(self):
        # before post there should be some validations
        self.prepost_validation()
        super(AccountMove, self).post()
    
    def prepost_validation(self):
        self._validate_end_date()
        self._validate_sequence()
        self._validate_quantity()
    
    def _validate_sequence_number(self, journal_name, move_count, number_next, max_range_number):
        if move_count and move_count + number_next - 1 > max_range_number:
            raise ValidationError(_('Consecutive range sold out. Contact the administrator to update the billing resolution. Journal: {}, Current Sequence: {}, invoices/credit notes count: {}, max range: {}'.format(journal_name, move_count, number_next, max_range_number)))

    def _validate_sequence(self):
        # group refund moves by its journal
        journals = {}
        for move in self.filtered(lambda m: m.journal_id and m.journal_id.type == 'sale'):
            if move.journal_id not in journals:
                journals[move.journal_id] = self.env['account.move']
            journals[move.journal_id] |= move

        for journal, moves in journals.items():
            if not journal.refund_sequence:
                self._validate_sequence_number(journal.name, len(moves), journal.sequence_number_next, journal.l10n_co_edi_max_range_number)
            else:
                invoices, refunds = moves.filtered(lambda move: move.type in ('in_invoice', 'out_invoice', 'in_receipt', 'out_receipt')), moves.filtered(lambda move: move.type in ('in_refund', 'out_refund'))
                self._validate_sequence_number(journal.name, len(invoices), journal.sequence_number_next, journal.l10n_co_edi_max_range_number)
                self._validate_sequence_number(journal.name, len(refunds), journal.refund_sequence_number_next, journal.l10n_co_edi_max_range_number)

    def _validate_end_date(self):
        invalid = self.filtered(lambda move: move.journal_id and move.journal_id.l10n_co_edi_dian_authorization_end_date and (move.invoice_date or date.today()) > move.journal_id.l10n_co_edi_dian_authorization_end_date)
        if invalid:
            raise ValidationError(_('The date of the invoice / credit note / debit note is not within the range valid by the DIAN'))

    def _validate_quantity(self):
        for move in self.filtered(lambda m: m.reversed_entry_id):
            origin = move.reversed_entry_id
            origin_product_qty = origin._group_product_qty()
            move_product_qty = move._group_product_qty()
            for product,uom_qty in move_product_qty.items():
                uom, qty = uom_qty
                ouom, oqty = origin_product_qty.get(product, [uom, 0.0])
                if float_compare(oqty, uom._compute_quantity(qty, ouom), precision_rounding=ouom.rounding) == -1:
                    raise ValidationError(_('The amounts to be returned cannot be greater than the amounts recorded in the sales invoice.'))

    def _group_product_qty(self):
        self.ensure_one()
        ret = {}
        for line in self.invoice_line_ids:
            if line.product_id not in ret:
                ret[line.product_id] = [line.product_uom_id, line.quantity]
            else:
                uom, qty = ret.get(line.product_id)
                quantity = line.product_uom_id._compute_quantity(line.quantity, uom)
                ret[line.product_id][1] = qty + quantity
        return ret
            
