from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class FireExtinguisher(models.Model):
    _name = 'fire.extinguisher'
    _description = 'Fire Extinguisher'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Serial Number', required=True, tracking=True)
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                default=lambda self: self.env.company)
    location = fields.Char(string='Location', required=True, tracking=True)
    building = fields.Char(string='Building', required=True)
    floor = fields.Char(string='Floor')
    
    type = fields.Selection([
        ('a', 'Class A - Ordinary Combustibles'),
        ('b', 'Class B - Flammable Liquids'),
        ('c', 'Class C - Electrical Equipment'),
        ('d', 'Class D - Combustible Metals'),
        ('k', 'Class K - Cooking Oils'),
        ('abc', 'Multi-Purpose ABC')
    ], string='Extinguisher Type', required=True)
    
    capacity = fields.Float(string='Capacity (kg)', required=True)
    manufacture_date = fields.Date(string='Manufacturing Date', required=True)
    installation_date = fields.Date(string='Installation Date', required=True)
    expiry_date = fields.Date(string='Expiry Date', required=True, tracking=True)
    last_inspection_date = fields.Date(string='Last Inspection Date')
    next_inspection_date = fields.Date(string='Next Inspection Date', compute='_compute_next_inspection',
                                     store=True)
    
    state = fields.Selection([
        ('active', 'Active'),
        ('maintenance', 'Under Maintenance'),
        ('expired', 'Expired'),
        ('replaced', 'Replaced')
    ], string='Status', default='active', tracking=True)
    
    maintenance_history_ids = fields.One2many('fire.extinguisher.maintenance', 'extinguisher_id',
                                            string='Maintenance History')
    notes = fields.Text(string='Notes')
    
    @api.depends('last_inspection_date')
    def _compute_next_inspection(self):
        for record in self:
            if record.last_inspection_date:
                record.next_inspection_date = fields.Date.from_string(record.last_inspection_date) + timedelta(days=90)
            else:
                record.next_inspection_date = False
    
    @api.constrains('manufacture_date', 'installation_date', 'expiry_date')
    def _check_dates(self):
        for record in self:
            if record.installation_date and record.manufacture_date and \
               record.installation_date < record.manufacture_date:
                raise ValidationError(_('Installation date cannot be before manufacturing date.'))
            if record.expiry_date and record.manufacture_date and \
               record.expiry_date < record.manufacture_date:
                raise ValidationError(_('Expiry date cannot be before manufacturing date.'))
    
    def action_set_maintenance(self):
        self.write({'state': 'maintenance'})
    
    def action_set_active(self):
        self.write({'state': 'active'})
    
    def action_set_expired(self):
        self.write({'state': 'expired'})
    
    def action_set_replaced(self):
        self.write({'state': 'replaced'})
    
    def action_schedule_maintenance(self):
        self.ensure_one()
        return {
            'name': _('Schedule Maintenance'),
            'type': 'ir.actions.act_window',
            'res_model': 'fire.extinguisher.maintenance',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_extinguisher_id': self.id,
                'default_maintenance_date': fields.Date.today(),
            }
        }

class FireExtinguisherMaintenance(models.Model):
    _name = 'fire.extinguisher.maintenance'
    _description = 'Fire Extinguisher Maintenance Record'
    _order = 'maintenance_date desc'

    extinguisher_id = fields.Many2one('fire.extinguisher', string='Fire Extinguisher',
                                     required=True, ondelete='cascade')
    company_id = fields.Many2one(related='extinguisher_id.company_id',
                                store=True, string='Company')
    maintenance_date = fields.Date(string='Maintenance Date', required=True,
                                 default=fields.Date.context_today)
    technician_id = fields.Many2one('res.users', string='Technician',
                                   default=lambda self: self.env.user, required=True)
    
    maintenance_type = fields.Selection([
        ('inspection', 'Regular Inspection'),
        ('refill', 'Refill'),
        ('repair', 'Repair'),
        ('certification', 'Certification')
    ], string='Maintenance Type', required=True)
    
    pressure_check = fields.Boolean(string='Pressure Check Passed')
    nozzle_check = fields.Boolean(string='Nozzle Check Passed')
    seal_check = fields.Boolean(string='Seal Check Passed')
    weight_check = fields.Boolean(string='Weight Check Passed')
    
    notes = fields.Text(string='Maintenance Notes')
    next_maintenance_date = fields.Date(string='Next Maintenance Due')
    
    @api.model_create_multi
    def create(self, vals_list):
        records = super(FireExtinguisherMaintenance, self).create(vals_list)
        for record in records:
            record.extinguisher_id.write({
                'last_inspection_date': record.maintenance_date
            })
        return records 