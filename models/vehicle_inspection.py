from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class VehicleInspection(models.Model):
    _name = 'vehicle.inspection'
    _description = 'Vehicle Safety Inspection'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'inspection_date desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                      default=lambda self: _('New'))
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                default=lambda self: self.env.company)
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle', required=True,
                               tracking=True)
    inspection_date = fields.Date(string='Inspection Date', required=True,
                                default=fields.Date.context_today)
    inspector_id = fields.Many2one('res.users', string='Inspector',
                                 default=lambda self: self.env.user, required=True)
    odometer = fields.Float(string='Odometer Reading', required=True)
    next_inspection_date = fields.Date(string='Next Inspection Due',
                                     compute='_compute_next_inspection_date', store=True)
    
    # Vehicle Information
    license_plate = fields.Char(related='vehicle_id.license_plate', string='License Plate',
                              readonly=True)
    vin_sn = fields.Char(related='vehicle_id.vin_sn', string='Chassis Number',
                        readonly=True)
    model_id = fields.Many2one(related='vehicle_id.model_id', string='Model',
                              readonly=True)
    
    # Inspection Checklist - Exterior
    body_condition = fields.Selection([
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor')
    ], string='Body Condition', required=True)
    windshield_condition = fields.Selection([
        ('good', 'Good'),
        ('cracked', 'Cracked'),
        ('damaged', 'Damaged')
    ], string='Windshield Condition', required=True)
    tire_condition = fields.Selection([
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor')
    ], string='Tire Condition', required=True)
    light_signals = fields.Boolean(string='Lights & Signals Working')
    
    # Inspection Checklist - Interior
    seat_belts = fields.Boolean(string='Seat Belts Working')
    mirrors = fields.Boolean(string='Mirrors in Good Condition')
    dashboard_lights = fields.Boolean(string='Dashboard Lights Working')
    horn = fields.Boolean(string='Horn Working')
    ac_heating = fields.Boolean(string='AC/Heating Working')
    
    # Inspection Checklist - Mechanical
    engine_condition = fields.Selection([
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor')
    ], string='Engine Condition', required=True)
    brake_condition = fields.Selection([
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor')
    ], string='Brake Condition', required=True)
    transmission = fields.Boolean(string='Transmission Working')
    steering = fields.Boolean(string='Steering System Working')
    exhaust = fields.Boolean(string='Exhaust System OK')
    
    # Safety Equipment
    first_aid_kit = fields.Boolean(string='First Aid Kit Present')
    fire_extinguisher = fields.Boolean(string='Fire Extinguisher Present')
    warning_triangle = fields.Boolean(string='Warning Triangle Present')
    spare_tire = fields.Boolean(string='Spare Tire Present')
    
    # Additional Information
    notes = fields.Text(string='Inspection Notes')
    recommendations = fields.Text(string='Recommendations')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('failed', 'Failed'),
        ('passed', 'Passed'),
        ('maintenance', 'Needs Maintenance')
    ], string='Status', default='draft', tracking=True)
    
    maintenance_ids = fields.One2many('vehicle.inspection.maintenance', 'inspection_id',
                                    string='Maintenance Items')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    
    @api.depends('inspection_date')
    def _compute_next_inspection_date(self):
        for record in self:
            if record.inspection_date:
                record.next_inspection_date = fields.Date.from_string(record.inspection_date) + timedelta(days=90)
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('vehicle.inspection') or _('New')
        return super(VehicleInspection, self).create(vals_list)
    
    def action_start_inspection(self):
        # Create a default maintenance record if none exists
        if not self.maintenance_ids:
            self.env['vehicle.inspection.maintenance'].create({
                'inspection_id': self.id,
                'vehicle_id': self.vehicle_id.id,
                'name': 'Initial Inspection',
                'priority': '1',
                'state': 'draft'
            })
        self.write({'state': 'in_progress'})
    
    def action_mark_failed(self):
        self.write({'state': 'failed'})
    
    def action_mark_passed(self):
        required_checks = [
            self.light_signals, self.seat_belts, self.mirrors, self.horn,
            self.transmission, self.steering, self.exhaust
        ]
        if not all(required_checks):
            raise ValidationError(_('All safety-critical checks must pass before marking inspection as passed.'))
        self.write({'state': 'passed'})
    
    def action_needs_maintenance(self):
        self.write({'state': 'maintenance'})
    
    def action_schedule_maintenance(self):
        return {
            'name': _('Schedule Maintenance'),
            'type': 'ir.actions.act_window',
            'res_model': 'vehicle.inspection.maintenance',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_inspection_id': self.id,
                'default_vehicle_id': self.vehicle_id.id,
            }
        }

class VehicleInspectionMaintenance(models.Model):
    _name = 'vehicle.inspection.maintenance'
    _description = 'Vehicle Inspection Maintenance Item'
    _order = 'priority desc, id desc'

    inspection_id = fields.Many2one('vehicle.inspection', string='Inspection',
                                  required=True)
    company_id = fields.Many2one(related='inspection_id.company_id',
                                store=True, string='Company')
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle', required=True)
    name = fields.Char(string='Maintenance Item', required=True)
    description = fields.Text(string='Description')
    
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
        ('3', 'Critical')
    ], string='Priority', required=True, default='1')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('done', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft')
    
    scheduled_date = fields.Date(string='Scheduled Date')
    completion_date = fields.Date(string='Completion Date')
    cost = fields.Float(string='Estimated Cost')
    notes = fields.Text(string='Notes')
    
    def action_schedule(self):
        if not self.scheduled_date:
            raise ValidationError(_('Please set a scheduled date before scheduling maintenance.'))
        self.write({'state': 'scheduled'})
    
    def action_start(self):
        self.write({'state': 'in_progress'})
    
    def action_complete(self):
        self.write({
            'state': 'done',
            'completion_date': fields.Date.today()
        })
    
    def action_cancel(self):
        self.write({'state': 'cancelled'}) 