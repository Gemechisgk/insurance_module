from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class InsuranceType(models.Model):
    _name = 'insurance.type'
    _description = 'Insurance Type'
    _order = 'name'

    name = fields.Char(string='Insurance Type', required=True)
    code = fields.Char(string='Code', required=True)
    description = fields.Text(string='Description')
    coverage_details = fields.Text(string='Coverage Details')
    company_id = fields.Many2one('res.company', string='Company',
                                default=lambda self: self.env.company)
    provider_ids = fields.Many2many('res.partner', string='Insurance Providers',
                                  domain=[('is_insurance_provider', '=', True)])
    active = fields.Boolean(default=True)

class InsuranceClaim(models.Model):
    _name = 'insurance.claim'
    _description = 'Insurance Claim'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'claim_date desc, id desc'

    name = fields.Char('Claim Reference', required=True, copy=False, readonly=True,
                      default=lambda self: _('New'))
    
    incident_id = fields.Many2one('incident.report', string='Related Incident',
                                 required=True, tracking=True)
    insurance_type_id = fields.Many2one('insurance.type', string='Insurance Type',
                                       required=True, tracking=True)
    claim_date = fields.Date('Claim Date', default=fields.Date.context_today,
                            required=True, tracking=True)
    amount = fields.Monetary('Claim Amount', required=True, tracking=True)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                 default=lambda self: self.env.company.currency_id)
    
    employee_id = fields.Many2one('hr.employee', string='Employee',
                                 required=True, tracking=True)
    department_id = fields.Many2one('hr.department', string='Department',
                                   related='employee_id.department_id', store=True)
    company_id = fields.Many2one('res.company', string='Company',
                                default=lambda self: self.env.company)
    
    description = fields.Text('Description', tracking=True)
    notes = fields.Text('Notes')
    document_ids = fields.Many2many('ir.attachment', string='Documents')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('processed', 'Processed'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('insurance.claim') or _('New')
        return super().create(vals_list)

    def action_submit(self):
        self.write({'state': 'submitted'})

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_process(self):
        self.write({'state': 'processed'})

    def action_reject(self):
        self.write({'state': 'rejected'})

    def action_reset_to_draft(self):
        self.write({'state': 'draft'})

    @api.constrains('amount')
    def _check_amount(self):
        for record in self:
            if record.amount <= 0:
                raise ValidationError(_("The claim amount must be positive."))

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            self.department_id = self.employee_id.department_id 