from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta

class IncidentInvestigator(models.Model):
    _name = 'incident.investigator'
    _description = 'Incident Investigator'
    _order = 'sequence, id'

    sequence = fields.Integer(string='Sequence', default=10)
    incident_id = fields.Many2one('incident.report', string='Incident Report', required=True, ondelete='cascade')
    employee_id = fields.Many2one('hr.employee', string='Investigator', required=True)
    designation = fields.Char(string='Designation', required=True)
    email = fields.Char(string='Email', related='employee_id.work_email', store=True, readonly=True)

    @api.onchange('employee_id')
    def _onchange_employee(self):
        if self.employee_id:
            self.designation = self.employee_id.job_title or ''
            self.email = self.employee_id.work_email or ''

class IncidentReport(models.Model):
    _name = 'incident.report'
    _description = 'Incident Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'incident_datetime desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                      default=lambda self: _('New'))
    
    # Section 1 - Personal/Employment Details
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    employee_id_number = fields.Char(string='Employee ID', readonly=True)
    address = fields.Text(string='Address', readonly=True)
    postcode = fields.Char(string='Postcode', readonly=True)
    date_of_birth = fields.Date(string='Date of Birth', readonly=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender', readonly=True)
    occupation = fields.Char(string='Occupation', readonly=True)
    time_in_job = fields.Char(string='Time in this Job')
    supervisor_id = fields.Many2one('hr.employee', string='Supervisor/Line Manager')
    employment_status = fields.Selection([
        ('full_time', 'Full Time'),
        ('contractual', 'Contractual')
    ], string='Employment Status', default='full_time')
    employer_name = fields.Char(string='Employer Name (if not company employee)')
    
    @api.onchange('employee_id')
    def _onchange_employee(self):
        if self.employee_id:
            self.employee_id_number = self.employee_id.id_number_generated
            self.address = self.employee_id.private_street
            self.postcode = self.employee_id.private_zip
            self.date_of_birth = self.employee_id.birthday
            self.gender = self.employee_id.gender
            self.occupation = self.employee_id.job_title
            self.supervisor_id = self.employee_id.parent_id
            self.employment_status = 'full_time'
            self.employer_name = False

    # Section 2 - Occurrence of the Incident
    incident_datetime = fields.Datetime(string='Date and Time', required=True, default=fields.Datetime.now)
    report_date = fields.Date(string='Date Reported', default=fields.Date.context_today)
    work_activity = fields.Text(string='Work Activity being performed')
    location = fields.Char(string='Exact Location of Incident', default='Not Specified')
    description = fields.Text(string='Incident Description', default='To be filled')
    witnesses = fields.Many2many('hr.employee', string='Witnesses')
    
    # Section 3 - Type of Injury
    incident_type = fields.Selection([
        ('mva', 'MVA'),
        ('pva', 'PVA'),
        ('motor_cyclist', 'Motor/Cyclist')
    ], string='Type of Incident')
    
    # Injury Types
    injury_strain_sprain = fields.Boolean(string='Strains/Sprains')
    injury_amputation = fields.Boolean(string='Amputation')
    injury_animal_bite = fields.Boolean(string='Animal/insect bite')
    injury_puncture = fields.Boolean(string='Puncture wound')
    injury_laceration = fields.Boolean(string='Lacerations/Abrasions')
    injury_hearing = fields.Boolean(string='Hearing Loss')
    injury_hernia = fields.Boolean(string='Hernia')
    injury_soft_tissue = fields.Boolean(string='Soft tissue injury')
    injury_contusion = fields.Boolean(string='Contusion (Bruise)')
    injury_foreign_body = fields.Boolean(string='Foreign body')
    injury_welding = fields.Boolean(string='Welding flash')
    injury_heat = fields.Boolean(string='Heat stress/Exhaustion')
    injury_burn_heat = fields.Boolean(string='Burns - heat')
    injury_burn_chemical = fields.Boolean(string='Burns - chemical')
    injury_burn_other = fields.Boolean(string='Burns - other')
    injury_dermatitis = fields.Boolean(string='Dermatitis (Skin rash)')
    injury_dental = fields.Boolean(string='Dental')
    injury_pain = fields.Boolean(string='Pain/Tenderness')
    injury_respiratory = fields.Boolean(string='Respiratory irritation')
    injury_twist = fields.Boolean(string='Twist')
    injury_disease = fields.Boolean(string='Disease')
    injury_toxic = fields.Boolean(string='Toxic reaction')
    injury_whiplash = fields.Boolean(string='Whip lash')
    injury_swelling = fields.Boolean(string='Swelling')
    injury_fracture = fields.Boolean(string='Fracture/Dislocation')
    injury_internal = fields.Boolean(string='Internal')
    injury_crush = fields.Boolean(string='Crush injury')
    injury_other = fields.Boolean(string='Other')
    injury_other_specify = fields.Char(string='Other Injury Specify')
    
    # Body Part Injured
    body_part_chest = fields.Boolean(string='Chest')
    body_part_abdomen = fields.Boolean(string='Abdomen')
    body_part_hip = fields.Boolean(string='Hip')
    body_part_genitals = fields.Boolean(string='Genitals')
    body_part_groin = fields.Boolean(string='Groin')
    body_part_circulatory = fields.Boolean(string='Circulatory')
    body_part_arm_upper = fields.Boolean(string='Arm upper')
    body_part_arm_lower = fields.Boolean(string='Arm lower')
    body_part_elbow = fields.Boolean(string='Elbow')
    body_part_wrist = fields.Boolean(string='Wrist')
    body_part_hand = fields.Boolean(string='Hand')
    body_part_shoulder = fields.Boolean(string='Shoulder')
    body_part_head = fields.Boolean(string='Head/Face')
    body_part_scalp = fields.Boolean(string='Scalp')
    body_part_nose = fields.Boolean(string='Nose')
    body_part_ears = fields.Boolean(string='Ears')
    body_part_eyes = fields.Boolean(string='Eyes')
    body_part_neck = fields.Boolean(string='Neck')
    body_part_back_upper = fields.Boolean(string='Back upper')
    body_part_back_middle = fields.Boolean(string='Back middle')
    body_part_back_lower = fields.Boolean(string='Back lower')
    body_part_leg_upper = fields.Boolean(string='Leg upper')
    body_part_leg_lower = fields.Boolean(string='Leg lower')
    body_part_knee = fields.Boolean(string='Knee')
    body_part_foot = fields.Boolean(string='Foot')
    body_part_ankle = fields.Boolean(string='Ankle')
    body_part_finger = fields.Boolean(string='Finger')
    body_part_toe = fields.Boolean(string='Toe')
    body_part_other = fields.Boolean(string='Other')
    body_part_other_specify = fields.Char(string='Other Body Part Specify')
    
    body_side = fields.Selection([
        ('left', 'Left'),
        ('right', 'Right'),
        ('multiple', 'Multiple')
    ], string='Part of Body Injured')
    
    # Section 4 - Property Damage
    property_damage_description = fields.Text(string='Description of damage')
    
    # Section 5 - Treatment
    treatment_required = fields.Selection([
        ('first_aid', 'First Aid'),
        ('doctor', 'Referred to Doctor'),
        ('hospital', 'Sent to Hospital'),
        ('returned', 'Returned to Work')
    ], string='Was any Treatment Required?')
    first_aid_attendant = fields.Char(string='First Aid Attendant')
    first_aid_treatment = fields.Text(string='First Aid Treatment Given')
    
    # Section 6 - Work Status
    work_status = fields.Selection([
        ('normal', 'Return to normal duties'),
        ('left', 'Left work – Home/Hospital/Doctor'),
        ('alternative', 'Alternative Duties')
    ], string='Work Status following injury')
    miss_shift = fields.Boolean(string='Is it likely that person may miss one complete shift?')
    
    # Additional Fields
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                default=lambda self: self.env.company)
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
    
    # Incident Investigators Section
    investigator_ids = fields.One2many('incident.investigator', 'incident_id', string='Investigators')
    
    # Incident Details
    nt_vehicles_involved = fields.Selection([
        ('1_truck', '1 Truck'),
        ('1_trailer', '1 Trailer'),
        ('1_truck_1_trailer', '1 Truck & 1 Trailer'),
        ('multiple', 'Multiple Vehicles')
    ], string='Number of NT owned vehicles involved')
    third_party_vehicles = fields.Boolean(string='3rd Party Vehicles Involved')
    incident_location = fields.Text(string='Incident Location (Address)')

    # Accident Details
    road_type = fields.Selection([
        ('national', 'National'),
        ('urban', 'Urban'),
        ('rural', 'Rural')
    ], string='Road Type')
    road_surface = fields.Selection([
        ('tar', 'Tar'),
        ('gravel', 'Gravel'),
        ('paved', 'Paved'),
        ('sand', 'Sand')
    ], string='Type of Road')
    road_condition = fields.Selection([
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor')
    ], string='Road Conditions')
    weather_condition = fields.Selection([
        ('dry', 'Dry'),
        ('wet', 'Wet'),
        ('rain', 'Rain'),
        ('extreme_heat', 'Extreme Heat'),
        ('extreme_cold', 'Extreme Cold')
    ], string='Weather Conditions')
    time_of_day = fields.Selection([
        ('day', 'Day'),
        ('night', 'Night'),
        ('dusk', 'Dusk'),
        ('dawn', 'Dawn')
    ], string='Time of Day')
    street_lighting = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
        ('na', 'N/A')
    ], string='Street Lighting')
    warning_given = fields.Boolean(string='Any Warning Given Before Accident')
    third_party_involved = fields.Boolean(string='3rd Party Involved')

    # Local Authority
    police_authority = fields.Boolean(string='Police Authority')
    case_number = fields.Char(string='Case Number')
    investigating_officer = fields.Char(string='Investigating Officer')
    officer_contact = fields.Char(string='Contact Details')
    arrests_charges = fields.Boolean(string='Arrests or Charges Laid')
    preliminary_findings = fields.Text(string='Preliminary Findings')

    # Vehicle Details
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle')
    vehicle_type = fields.Char(string='Vehicle Type', compute='_compute_vehicle_info', store=True)
    vehicle_ownership = fields.Selection([
        ('nt', 'NT'),
        ('contractor', 'Contractor')
    ], string='Vehicle Ownership', default='nt')
    vehicle_make = fields.Char(string='Make', compute='_compute_vehicle_info', store=True)
    vehicle_model = fields.Char(string='Model', compute='_compute_vehicle_info', store=True)
    odometer_reading = fields.Float(string='Odometer Reading (km)', compute='_compute_vehicle_info', store=True)
    damage_extent = fields.Selection([
        ('light', 'Light'),
        ('medium', 'Medium'),
        ('heavy', 'Heavy'),
        ('total', 'Total')
    ], string='Extent of Damage')
    service_records_available = fields.Boolean(string='Service/Maintenance Records Available', compute='_compute_vehicle_info', store=True)
    last_service_date = fields.Date(string='Date of Last Service', compute='_compute_last_service_date', store=True)
    vehicle_roadworthy = fields.Boolean(string='Was the vehicle roadworthy before incident?')
    product_carried = fields.Char(string='What product was the vehicle carrying?')
    load_secured = fields.Boolean(string='Load Secured for Transportation')
    load_correct = fields.Boolean(string='Was the vehicle loaded correctly?')
    product_handling = fields.Text(string='How was the product handled after the incident?')
    telematics_installed = fields.Boolean(string='Telematics/GPS Installed', compute='_compute_vehicle_info', store=True)

    @api.depends('vehicle_id', 'vehicle_id.model_id', 'vehicle_id.model_id.brand_id', 'vehicle_id.odometer')
    def _compute_vehicle_info(self):
        for record in self:
            if record.vehicle_id:
                record.vehicle_type = record.vehicle_id.model_id.brand_id.name if record.vehicle_id.model_id.brand_id else ''
                record.vehicle_make = record.vehicle_id.model_id.brand_id.name if record.vehicle_id.model_id.brand_id else ''
                record.vehicle_model = record.vehicle_id.model_id.name if record.vehicle_id.model_id else ''
                record.odometer_reading = record.vehicle_id.odometer or 0.0
                record.service_records_available = bool(record.vehicle_id.service_count)
                record.telematics_installed = record.vehicle_id.telematics_installed if hasattr(record.vehicle_id, 'telematics_installed') else False
            else:
                record.vehicle_type = ''
                record.vehicle_make = ''
                record.vehicle_model = ''
                record.odometer_reading = 0.0
                record.service_records_available = False
                record.telematics_installed = False

    @api.depends('vehicle_id')
    def _compute_last_service_date(self):
        for record in self:
            if record.vehicle_id:
                last_service = self.env['fleet.vehicle.log.services'].search([
                    ('vehicle_id', '=', record.vehicle_id.id)
                ], order='date desc', limit=1)
                record.last_service_date = last_service.date if last_service else False
            else:
                record.last_service_date = False

    # Telematics/GPS Data
    telematics_start_time = fields.Datetime(string='Start time (Day of Incident)')
    telematics_end_time = fields.Datetime(string='End Time (Incident)')
    time_travelled = fields.Float(string='Time Travelled for the day (hours)')
    distance_travelled = fields.Float(string='Distance Travelled (km)')
    speed_before_accident = fields.Float(string='Speed Before Accident (km/h)')
    speed_at_incident = fields.Float(string='Speed at Time of Incident (km/h)')
    max_speed = fields.Float(string='Maximum Speed (km/h)')
    speed_violations = fields.Integer(string='Speed Violations for day')
    harsh_braking = fields.Integer(string='Harsh Braking for day')
    driver_history = fields.Text(string='Driver History (30 Days)')

    # Driver Details
    driver_id = fields.Many2one('hr.employee', string='Driver', required=True)
    driver_name = fields.Char(string='Full Name', compute='_compute_driver_info', store=True)
    driver_age = fields.Integer(string='Age', compute='_compute_driver_info', store=True)
    driver_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender', compute='_compute_driver_info', store=True)
    employment_period = fields.Char(string='Period Employed')
    employment_history = fields.Text(string='Employment History (External)')
    driver_statement = fields.Boolean(string='Driver\'s Incident Statement obtained')
    license_valid = fields.Boolean(string='Is license valid for vehicle type?')
    medical_fitness = fields.Boolean(string='Medical Fitness Certificate')
    medical_deviations = fields.Boolean(string='Any deviations found on medical?')
    sick_leave_history = fields.Text(string='Leave/Sick Leave History (Past 6 Months)')
    medicine_taken = fields.Boolean(string='Medicine taken on day of accident')
    total_driving_time = fields.Float(string='Total Driving Time for day (hours)')
    six_month_performance = fields.Text(string='6 Month Performance')
    root_cause = fields.Text(string='Root Cause Identified')

    # Source of Information
    source_telematics = fields.Boolean(string='Telematics/GPS data')
    source_police_report = fields.Boolean(string='Traffic Police Report')
    source_maintenance = fields.Boolean(string='Truck Maintenance History')
    source_field_report = fields.Boolean(string='Field report')

    # Signatures
    fleet_manager_name = fields.Char(string='Fleet Operation Department Manager Name')
    fleet_manager_signature = fields.Binary(string='Fleet Operation Department Manager Signature')
    fleet_manager_date = fields.Date(string='Fleet Operation Department Manager Date')

    planning_manager_name = fields.Char(string='Planning & Safety Department Manager Name')
    planning_manager_signature = fields.Binary(string='Planning & Safety Department Manager Signature')
    planning_manager_date = fields.Date(string='Planning & Safety Department Manager Date')

    maintenance_manager_name = fields.Char(string='E & Maintenance Department Manager Name')
    maintenance_manager_signature = fields.Binary(string='E & Maintenance Department Manager Signature')
    maintenance_manager_date = fields.Date(string='E & Maintenance Department Manager Date')

    @api.depends('incident_type')
    def _compute_requires_investigation(self):
        for record in self:
            record.requires_investigation = record.incident_type in ['mva', 'pva']
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('incident.report') or _('New')
            # Set default values for required fields if not provided
            if 'description' not in vals:
                vals['description'] = 'To be filled'
            if 'location' not in vals:
                vals['location'] = 'Not Specified'
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

    @api.depends('driver_id', 'driver_id.birthday', 'driver_id.gender')
    def _compute_driver_info(self):
        for record in self:
            if record.driver_id:
                # Compute age
                if record.driver_id.birthday:
                    today = fields.Date.today()
                    age = today.year - record.driver_id.birthday.year
                    if today.month < record.driver_id.birthday.month or (today.month == record.driver_id.birthday.month and today.day < record.driver_id.birthday.day):
                        age -= 1
                    record.driver_age = age
                else:
                    record.driver_age = 0

                # Set other fields
                record.driver_name = record.driver_id.name
                record.driver_gender = record.driver_id.gender
            else:
                record.driver_name = ''
                record.driver_age = 0
                record.driver_gender = False 