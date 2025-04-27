from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class EmployeeSuggestion(models.Model):
    _name = 'employee.suggestion'
    _description = 'Employee Safety Suggestion'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'submission_date desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                      default=lambda self: _('New'))
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                default=lambda self: self.env.company)
    employee_id = fields.Many2one('hr.employee', string='Employee',
                                default=lambda self: self.env.user.employee_id)
    department_id = fields.Many2one('hr.department', string='Department',
                                  related='employee_id.department_id', store=True)
    
    submission_date = fields.Date(string='Submission Date', required=True,
                                default=fields.Date.context_today)
    category = fields.Selection([
        ('workplace', 'Workplace Safety'),
        ('equipment', 'Equipment Safety'),
        ('procedure', 'Safety Procedures'),
        ('training', 'Safety Training'),
        ('emergency', 'Emergency Preparedness'),
        ('other', 'Other')
    ], string='Category', required=True)
    
    suggestion_type = fields.Selection([
        ('improvement', 'Improvement Suggestion'),
        ('hazard', 'Hazard Report'),
        ('prevention', 'Prevention Measure'),
        ('training', 'Training Need')
    ], string='Suggestion Type', required=True)
    
    title = fields.Char(string='Suggestion Title', required=True)
    description = fields.Text(string='Description', required=True)
    current_situation = fields.Text(string='Current Situation')
    proposed_solution = fields.Text(string='Proposed Solution')
    expected_benefits = fields.Text(string='Expected Benefits')
    
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
        ('3', 'Critical')
    ], string='Priority', required=True, default='1')
    
    anonymous = fields.Boolean(string='Submit Anonymously')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('implemented', 'Implemented'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', tracking=True)
    
    reviewer_id = fields.Many2one('res.users', string='Reviewer')
    review_date = fields.Date(string='Review Date')
    review_notes = fields.Text(string='Review Notes')
    implementation_date = fields.Date(string='Implementation Date')
    rejection_reason = fields.Text(string='Rejection Reason')
    
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    
    # Implementation Plan
    implementation_plan_ids = fields.One2many('suggestion.implementation.plan',
                                            'suggestion_id',
                                            string='Implementation Plan')
    
    cost_estimate = fields.Float(string='Cost Estimate')
    implementation_time = fields.Integer(string='Implementation Time (days)')
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('employee.suggestion') or _('New')
            if vals.get('anonymous', False):
                vals['employee_id'] = False
        return super(EmployeeSuggestion, self).create(vals_list)
    
    def action_submit(self):
        if not self.description or not self.title:
            raise ValidationError(_('Please provide both title and description before submitting.'))
        self.write({'state': 'submitted'})
    
    def action_review(self):
        self.write({
            'state': 'under_review',
            'reviewer_id': self.env.user.id,
            'review_date': fields.Date.today()
        })
    
    def action_approve(self):
        if not self.review_notes:
            raise ValidationError(_('Please add review notes before approving.'))
        self.write({'state': 'approved'})
    
    def action_implement(self):
        if not self.implementation_plan_ids:
            raise ValidationError(_('Please create an implementation plan before marking as implemented.'))
        self.write({
            'state': 'implemented',
            'implementation_date': fields.Date.today()
        })
    
    def action_reject(self):
        if not self.rejection_reason:
            raise ValidationError(_('Please provide a rejection reason.'))
        self.write({'state': 'rejected'})
    
    def action_reset_to_draft(self):
        self.write({'state': 'draft'})

class SuggestionImplementationPlan(models.Model):
    _name = 'suggestion.implementation.plan'
    _description = 'Suggestion Implementation Plan'
    _order = 'sequence'

    suggestion_id = fields.Many2one('employee.suggestion', string='Suggestion',
                                  required=True)
    company_id = fields.Many2one(related='suggestion_id.company_id',
                                store=True, string='Company')
    sequence = fields.Integer(string='Sequence', default=10)
    name = fields.Char(string='Action Item', required=True)
    description = fields.Text(string='Description')
    
    responsible_id = fields.Many2one('res.users', string='Responsible Person')
    deadline = fields.Date(string='Deadline')
    
    state = fields.Selection([
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='planned')
    
    completion_date = fields.Date(string='Completion Date')
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