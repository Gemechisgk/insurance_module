from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class VehicleInspection(models.Model):
    _name = 'vehicle.inspection'
    _description = 'Vehicle Inspection'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'inspection_date desc'

    name = fields.Char(string='Inspection Reference', required=True, copy=False, readonly=True, default=lambda self: ('New'))
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle', required=True, tracking=True)
    inspection_date = fields.Date(string='Inspection Date', default=fields.Date.context_today, tracking=True)
    inspector_id = fields.Many2one('res.users', string='Inspector', default=lambda self: self.env.user, tracking=True)
    mileage = fields.Float(string='Mileage (Km/Hr)', tracking=True)

    # Service Brake System
    service_brake_status = fields.Selection([
        ('ok', 'OK'),
        ('defective', 'Defective')
    ], string='Service Brake Status', tracking=True)

    # Parking Brake System
    parking_brake_status = fields.Selection([
        ('ok', 'OK'),
        ('defective', 'Defective')
    ], string='Parking Brake Status', tracking=True)

    # Door Locks
    door_front_left_status = fields.Selection([
        ('ok', 'OK'),
        ('defective', 'Defective')
    ], string='Front Left Door Status', tracking=True)
    door_front_right_status = fields.Selection([
        ('ok', 'OK'),
        ('defective', 'Defective')
    ], string='Front Right Door Status', tracking=True)
    door_rear_left_status = fields.Selection([
        ('ok', 'OK'),
        ('defective', 'Defective')
    ], string='Rear Left Door Status', tracking=True)
    door_rear_right_status = fields.Selection([
        ('ok', 'OK'),
        ('defective', 'Defective')
    ], string='Rear Right Door Status', tracking=True)
    door_hatch_status = fields.Selection([
        ('ok', 'OK'),
        ('defective', 'Defective')
    ], string='Hatch Back Status', tracking=True)

    # Seat Belts
    seat_belt_front_left_status = fields.Selection([
        ('ok', 'OK'),
        ('defective', 'Defective'),
        ('missing', 'Missing')
    ], string='Front Left Seat Belt Status', tracking=True)
    seat_belt_front_right_status = fields.Selection([
        ('ok', 'OK'),
        ('defective', 'Defective'),
        ('missing', 'Missing')
    ], string='Front Right Seat Belt Status', tracking=True)

    # Center Rear View Mirror
    rear_view_mirror_status = fields.Selection([
        ('ok', 'OK'),
        ('defective', 'Defective'),
        ('missing', 'Missing')
    ], string='Rear View Mirror Status', tracking=True)

    # Lighting System
    headlight_r_high_status = fields.Selection([
        ('ok', 'OK'),
        ('fade', 'Fade-out'),
        ('defective', 'Defective')
    ], string='Right Headlight High Beam Status', tracking=True)
    headlight_r_low_status = fields.Selection([
        ('ok', 'OK'),
        ('fade', 'Fade-out'),
        ('defective', 'Defective')
    ], string='Right Headlight Low Beam Status', tracking=True)
    headlight_l_high_status = fields.Selection([
        ('ok', 'OK'),
        ('fade', 'Fade-out'),
        ('defective', 'Defective')
    ], string='Left Headlight High Beam Status', tracking=True)
    headlight_l_low_status = fields.Selection([
        ('ok', 'OK'),
        ('fade', 'Fade-out'),
        ('defective', 'Defective')
    ], string='Left Headlight Low Beam Status', tracking=True)

    # Side Mirrors
    side_mirror_left_status = fields.Selection([
        ('ok', 'OK'),
        ('defective', 'Defective'),
        ('missing', 'Missing')
    ], string='Left Side Mirror Status', tracking=True)
    side_mirror_right_status = fields.Selection([
        ('ok', 'OK'),
        ('defective', 'Defective'),
        ('missing', 'Missing')
    ], string='Right Side Mirror Status', tracking=True)

    # Wind Shield
    windshield_left_status = fields.Selection([
        ('ok', 'OK'),
        ('defective', 'Defective'),
        ('missing', 'Missing')
    ], string='Left Windshield Status', tracking=True)
    windshield_right_status = fields.Selection([
        ('ok', 'OK'),
        ('defective', 'Defective'),
        ('missing', 'Missing')
    ], string='Right Windshield Status', tracking=True)

    # Wiper
    wiper_left_status = fields.Selection([
        ('ok', 'OK'),
        ('defective', 'Defective'),
        ('missing', 'Missing')
    ], string='Left Wiper Status', tracking=True)
    wiper_right_status = fields.Selection([
        ('ok', 'OK'),
        ('defective', 'Defective'),
        ('missing', 'Missing')
    ], string='Right Wiper Status', tracking=True)

    # Dashboard
    warning_lamps_status = fields.Selection([
        ('ok', 'OK'),
        ('defective', 'Defective')
    ], string='Warning Lamps Status', tracking=True)
    gauges_status = fields.Selection([
        ('ok', 'OK'),
        ('defective', 'Defective')
    ], string='Gauges Status', tracking=True)
    mileage_info_status = fields.Selection([
        ('ok', 'OK'),
        ('defective', 'Defective')
    ], string='Mileage Info Status', tracking=True)
    fire_extinguisher_status = fields.Selection([
        ('ok', 'OK'),
        ('defective', 'Defective')
    ], string='Fire Extinguisher Status', tracking=True)
    first_aid_kit_status = fields.Selection([
        ('ok', 'OK'),
        ('defective', 'Defective')
    ], string='First Aid Kit Status', tracking=True)

    findings = fields.Text(string='Inspection Results', tracking=True)
    recommendations = fields.Text(string='Recommendations', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    maintenance_ids = fields.One2many('vehicle.inspection.maintenance', 'inspection_id', string='Maintenance Items')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')

    @api.depends('inspection_date')
    def _compute_next_inspection_date(self):
        for record in self:
            if record.inspection_date:
                record.next_inspection_date = fields.Date.from_string(record.inspection_date) + timedelta(days=90)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('vehicle.inspection') or 'New'
        return super().create(vals_list)

    def action_draft(self):
        self.write({'state': 'draft'})

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

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

    def print_report(self):
        return self.env.ref('insurance_module.action_report_vehicle_inspection').report_action(self)

class VehicleInspectionMaintenance(models.Model):
    _name = 'vehicle.inspection.maintenance'
    _description = 'Vehicle Inspection Maintenance Item'
    _order = 'priority desc, id desc'

    inspection_id = fields.Many2one('vehicle.inspection', string='Inspection', required=True)
    company_id = fields.Many2one(related='inspection_id.company_id', store=True, string='Company')
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