from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class WeldingMachineInspection(models.Model):
    _name = 'welding.machine.inspection'
    _description = 'Welding Machine Inspection'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'inspection_date desc'

    name = fields.Char(string='Document No.', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    inspection_date = fields.Date(string='Date of Inspection', required=True, default=fields.Date.context_today, tracking=True)
    inspector_id = fields.Many2one('res.users', string='Inspection Done By', required=True, default=lambda self: self.env.user, tracking=True)
    reviewer_id = fields.Many2one('res.users', string='Reviewed by')
    sign_inspector = fields.Char(string='Sign with date (Inspector)')
    sign_reviewer = fields.Char(string='Sign with date (Reviewer)')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    # Checklist fields
    checklist_1 = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='1. Welding machine should be physically sound and in working condition. Eg proper cover in all side')
    comments_1 = fields.Char(string='Comments 1')

    checklist_2 = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='2. Switches and power breaker should be free from damage and properly insulated.')
    comments_2 = fields.Char(string='Comments 2')

    checklist_3 = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='3. Welding and return led cable should be mechanically strong and Electrically adequate connection should be properly tight by means of socket/terminal lugs.')
    comments_3 = fields.Char(string='Comments 3')

    checklist_4 = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='4. Welding and return led should be free from damage for eg. Cut, Open, too many joints, etc..')
    comments_4 = fields.Char(string='Comments 4')

    checklist_5 = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='5. Welding holder should be in good condition without any metal contact.')
    comments_5 = fields.Char(string='Comments 5')

    checklist_6 = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='6. All Cable should be damage free and always use industrial plug to take power connection.')
    comments_6 = fields.Char(string='Comments 6')

    notes = fields.Text(string='Additional Notes')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('welding.machine.inspection') or _('New')
        return super(WeldingMachineInspection, self).create(vals_list)

    def action_start_inspection(self):
        self.write({'state': 'in_progress'})

    def action_complete_inspection(self):
        # Optionally, require all checklist items to be answered
        self.write({'state': 'done'})

    def action_cancel_inspection(self):
        self.write({'state': 'cancelled'})

    def action_reset_to_draft(self):
        self.write({'state': 'draft'})

    def print_report(self):
        return self.env.ref('insurance_module.action_report_welding_machine_inspection').report_action(self) 