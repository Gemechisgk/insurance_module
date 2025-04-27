from odoo import models, fields, api

class InsuranceType(models.Model):
    _name = 'insurance.type'
    _description = 'Insurance Type'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=True)
    code = fields.Char(string='Code', required=True, tracking=True)
    description = fields.Text(string='Description', tracking=True)
    company_id = fields.Many2one('res.company', string='Company', 
        default=lambda self: self.env.company) 