from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class AccidentInvestigation(models.Model):
    _name = 'accident.investigation'
    _description = 'Accident Investigation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'investigation_date desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                      default=lambda self: _('New'))
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                default=lambda self: self.env.company)
    incident_id = fields.Many2one('incident.report', string='Related Incident',
                                required=True, tracking=True)
    investigation_date = fields.Date(string='Investigation Date', required=True,
                                   default=fields.Date.context_today)
    investigator_ids = fields.Many2many('res.users', string='Investigation Team',
                                      required=True)
    
    # Investigation Details
    incident_description = fields.Text(string='Incident Description',
                                     related='incident_id.description', readonly=True)
    root_cause = fields.Text(string='Root Cause Analysis', required=True)
    contributing_factors = fields.Text(string='Contributing Factors')
    
    # Investigation Findings
    immediate_causes = fields.Text(string='Immediate Causes')
    underlying_causes = fields.Text(string='Underlying Causes')
    basic_causes = fields.Text(string='Basic Causes')
    
    # Evidence Collection
    physical_evidence = fields.Text(string='Physical Evidence')
    witness_statements = fields.Text(string='Witness Statements')
    document_review = fields.Text(string='Document Review')
    
    # Corrective Actions
    corrective_action_ids = fields.One2many('investigation.corrective.action',
                                          'investigation_id',
                                          string='Corrective Actions')
    
    # Recommendations
    recommendations = fields.Text(string='Recommendations')
    preventive_measures = fields.Text(string='Preventive Measures')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('review', 'Under Review'),
        ('approved', 'Approved'),
        ('closed', 'Closed')
    ], string='Status', default='draft', tracking=True)
    
    attachment_ids = fields.Many2many('ir.attachment', string='Investigation Documents')
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('accident.investigation') or _('New')
        return super(AccidentInvestigation, self).create(vals_list)
    
    def action_start_investigation(self):
        self.write({'state': 'in_progress'})
    
    def action_submit_review(self):
        if not self.corrective_action_ids:
            raise ValidationError(_('At least one corrective action must be defined before submitting for review.'))
        self.write({'state': 'review'})
    
    def action_approve(self):
        self.write({'state': 'approved'})
    
    def action_close(self):
        if any(action.state != 'completed' for action in self.corrective_action_ids):
            raise ValidationError(_('All corrective actions must be completed before closing the investigation.'))
        self.write({'state': 'closed'})
        self.incident_id.write({'state': 'resolved'})

class InvestigationCorrectiveAction(models.Model):
    _name = 'investigation.corrective.action'
    _description = 'Investigation Corrective Action'
    _order = 'deadline'

    investigation_id = fields.Many2one('accident.investigation',
                                     string='Investigation', required=True)
    company_id = fields.Many2one(related='investigation_id.company_id',
                                store=True, string='Company')
    name = fields.Char(string='Action Item', required=True)
    description = fields.Text(string='Description')
    
    action_type = fields.Selection([
        ('immediate', 'Immediate Action'),
        ('short_term', 'Short Term Action'),
        ('long_term', 'Long Term Action')
    ], string='Action Type', required=True)
    
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
        ('3', 'Critical')
    ], string='Priority', required=True)
    
    responsible_id = fields.Many2one('res.users', string='Responsible Person',
                                   required=True)
    deadline = fields.Date(string='Deadline', required=True)
    completion_date = fields.Date(string='Completion Date')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    
    notes = fields.Text(string='Notes')
    
    def action_start(self):
        self.write({'state': 'in_progress'})
    
    def action_complete(self):
        self.write({
            'state': 'completed',
            'completion_date': fields.Date.today()
        })
    
    def action_cancel(self):
        self.write({'state': 'cancelled'}) 