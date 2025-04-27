from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class OfficeInspection(models.Model):
    _name = 'office.inspection'
    _description = 'Office Safety Inspection'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'inspection_date desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                      default=lambda self: _('New'))
    inspection_date = fields.Date(string='Inspection Date', required=True, tracking=True,
                                default=fields.Date.context_today)
    inspector_id = fields.Many2one('res.users', string='Safety Officer', required=True,
                                 default=lambda self: self.env.user, tracking=True)
    department_id = fields.Many2one('hr.department', string='Department', required=True)
    location = fields.Char(string='Location', required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                default=lambda self: self.env.company)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    # Inspection Checklist
    fire_safety_ok = fields.Boolean(string='Fire Safety Equipment')
    emergency_exits_ok = fields.Boolean(string='Emergency Exits')
    first_aid_ok = fields.Boolean(string='First Aid Kits')
    electrical_safety_ok = fields.Boolean(string='Electrical Safety')
    workspace_safety_ok = fields.Boolean(string='Workspace Safety')
    
    notes = fields.Text(string='Inspection Notes')
    recommendation = fields.Text(string='Recommendations')
    
    # Corrective Actions
    corrective_action_ids = fields.One2many('office.inspection.action', 'inspection_id',
                                          string='Corrective Actions')
    
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('office.inspection') or _('New')
        return super(OfficeInspection, self).create(vals_list)
    
    def action_start_inspection(self):
        self.write({'state': 'in_progress'})
    
    def action_complete_inspection(self):
        if not all([self.fire_safety_ok, self.emergency_exits_ok, self.first_aid_ok,
                   self.electrical_safety_ok, self.workspace_safety_ok]):
            raise ValidationError(_('All safety checks must be completed before marking as done.'))
        self.write({'state': 'done'})
    
    def action_cancel_inspection(self):
        self.write({'state': 'cancelled'})
    
    def action_reset_to_draft(self):
        self.write({'state': 'draft'})

class OfficeInspectionAction(models.Model):
    _name = 'office.inspection.action'
    _description = 'Corrective Action for Office Inspection'
    _order = 'deadline'

    inspection_id = fields.Many2one('office.inspection', string='Inspection', required=True)
    name = fields.Char(string='Action Item', required=True)
    responsible_id = fields.Many2one('res.users', string='Responsible Person', required=True)
    deadline = fields.Date(string='Deadline', required=True)
    company_id = fields.Many2one('res.company', string='Company', related='inspection_id.company_id',
                                store=True, index=True)
    state = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Completed'),
    ], string='Status', default='pending', tracking=True)
    notes = fields.Text(string='Notes')
    completion_date = fields.Date(string='Completion Date')

    def action_mark_as_done(self):
        self.write({
            'state': 'done',
            'completion_date': fields.Date.today()
        }) 