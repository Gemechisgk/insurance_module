from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class IncidentReport(models.Model):
    _name = 'incident.report'
    _description = 'Incident Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'incident_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                      default=lambda self: _('New'))
    incident_date = fields.Datetime(string='Incident Date & Time', required=True,
                                  default=fields.Datetime.now, tracking=True)
    reported_by_id = fields.Many2one('res.users', string='Reported By',
                                   default=lambda self: self.env.user, required=True)
    department_id = fields.Many2one('hr.department', string='Department', required=True)
    location = fields.Char(string='Location', required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                default=lambda self: self.env.company)
    
    incident_type = fields.Selection([
        ('fire', 'Fire Incident'),
        ('injury', 'Personal Injury'),
        ('equipment', 'Equipment Failure'),
        ('security', 'Security Breach'),
        ('environmental', 'Environmental Incident'),
        ('other', 'Other')
    ], string='Incident Type', required=True)
    
    severity = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], string='Severity Level', required=True)
    
    description = fields.Text(string='Incident Description', required=True)
    immediate_action = fields.Text(string='Immediate Actions Taken')
    witnesses = fields.Many2many('hr.employee', string='Witnesses')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('reported', 'Reported'),
        ('investigation', 'Under Investigation'),
        ('action', 'Action Required'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed')
    ], string='Status', default='draft', tracking=True)
    
    requires_investigation = fields.Boolean(string='Requires Investigation',
                                         compute='_compute_requires_investigation', store=True)
    investigation_ids = fields.One2many('accident.investigation', 'incident_id',
                                      string='Investigations')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    
    # Insurance Claim Related Fields
    insurance_claim_required = fields.Boolean(string='Insurance Claim Required')
    insurance_claim_id = fields.Many2one('insurance.claim', string='Insurance Claim')
    police_report_required = fields.Boolean(string='Police Report Required')
    police_report_number = fields.Char(string='Police Report Number')
    
    @api.depends('severity', 'incident_type')
    def _compute_requires_investigation(self):
        for record in self:
            record.requires_investigation = (
                record.severity in ['high', 'critical'] or
                record.incident_type in ['fire', 'injury']
            )
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('incident.report') or _('New')
        return super(IncidentReport, self).create(vals_list)
    
    def action_report(self):
        self.write({'state': 'reported'})
        if self.requires_investigation:
            self.write({'state': 'investigation'})
            # Create investigation record
            self.env['accident.investigation'].create({
                'incident_id': self.id,
                'name': f'Investigation for {self.name}',
                'investigation_date': fields.Date.today(),
            })
    
    def action_start_investigation(self):
        self.write({'state': 'investigation'})
    
    def action_mark_action_required(self):
        self.write({'state': 'action'})
    
    def action_resolve(self):
        self.write({'state': 'resolved'})
    
    def action_close(self):
        if self.requires_investigation and not self.investigation_ids:
            raise ValidationError(_('Cannot close incident that requires investigation without completing the investigation.'))
        self.write({'state': 'closed'})
    
    def action_create_insurance_claim(self):
        if not self.insurance_claim_id:
            claim = self.env['insurance.claim'].create({
                'incident_id': self.id,
                'name': f'Claim for {self.name}',
                'claim_date': fields.Date.today(),
            })
            self.write({'insurance_claim_id': claim.id}) 