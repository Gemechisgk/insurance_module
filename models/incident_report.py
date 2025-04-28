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
    department_id = fields.Many2one('hr.department', string='Department', required=True)
    supervisor_id = fields.Many2one('hr.employee', string='Supervisor/Line Manager')
    employment_status = fields.Selection([
        ('full_time', 'Full Time'),
        ('contractual', 'Contractual')
    ], string='Employment Status', required=True)
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
            self.department_id = self.employee_id.department_id
            self.supervisor_id = self.employee_id.parent_id
            # Set default employment status to full_time
            self.employment_status = 'full_time'
            self.employer_name = False

    # Section 2 - Occurrence of the Incident
    incident_date = fields.Datetime(string='Date of Incident', required=True,
                                  default=fields.Datetime.now, tracking=True)
    incident_time = fields.Float(string='Time of Incident')
    report_date = fields.Date(string='Date Reported', default=fields.Date.context_today)
    work_activity = fields.Text(string='Work Activity being performed')
    location = fields.Char(string='Exact Location of Incident', required=True)
    description = fields.Text(string='Incident Description', required=True)
    witnesses = fields.Many2many('hr.employee', string='Witnesses')
    
    # Section 3 - Type of Injury
    incident_type = fields.Selection([
        ('injury', 'Injury'),
        ('property_damage', 'Property Damage'),
        ('near_miss', 'Near Miss')
    ], string='Incident Type', required=True)
    
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
    
    @api.depends('incident_type')
    def _compute_requires_investigation(self):
        for record in self:
            record.requires_investigation = record.incident_type in ['injury', 'property_damage']
    
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