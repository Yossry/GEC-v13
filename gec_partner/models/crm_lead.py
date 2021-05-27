from odoo import api, fields, models
from odoo.exceptions import UserError

class CrmLead(models.Model):
    _inherit = "crm.lead"

    state_id = fields.Many2one("res.country.state", string='Estado')