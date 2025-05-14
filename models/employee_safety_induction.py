from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class EmployeeSafetyInduction(models.Model):
    _name = 'employee.safety.induction'
    _description = 'Employee Safety Induction'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Reference', required=True, copy=False, 
                      readonly=True, default=lambda self: ('New'))
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, tracking=True)
    date = fields.Date(string='Induction Date', required=True, default=fields.Date.context_today, tracking=True)
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one('res.company', string='Company', 
                                default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('employee.safety.induction') or 'New'
        return super().create(vals_list)

    def action_complete(self):
        if not self.attachment_ids:
            raise ValidationError(_('Please attach at least one document before completing the induction.'))
        self.write({'state': 'completed'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_draft(self):
        self.write({'state': 'draft'}) 