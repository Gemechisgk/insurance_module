from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_insurance_provider = fields.Boolean(
        string='Is Insurance Provider',
        default=False,
        help='Check this box if this contact is an Insurance Provider'
    ) 