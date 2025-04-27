from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_auto_inspection_reminder = fields.Boolean(
        string='Automatic Inspection Reminders',
        help='Enable automatic reminders for inspections'
    )
    module_safety_dashboard = fields.Boolean(
        string='Safety Dashboard',
        help='Enable safety dashboard with KPIs'
    )
    module_insurance_claim_automation = fields.Boolean(
        string='Insurance Claim Automation',
        help='Enable automated claim processing workflow'
    )
    module_insurance_analytics = fields.Boolean(
        string='Insurance Analytics',
        help='Enable insurance analytics and reporting'
    )
    module_vehicle_maintenance_reminder = fields.Boolean(
        string='Vehicle Maintenance Reminders',
        help='Enable vehicle maintenance reminders'
    )
    module_safety_training_management = fields.Boolean(
        string='Safety Training Management',
        help='Enable safety training management'
    )

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('insurance_module.module_auto_inspection_reminder', self.module_auto_inspection_reminder)
        self.env['ir.config_parameter'].sudo().set_param('insurance_module.module_safety_dashboard', self.module_safety_dashboard)
        self.env['ir.config_parameter'].sudo().set_param('insurance_module.module_insurance_claim_automation', self.module_insurance_claim_automation)
        self.env['ir.config_parameter'].sudo().set_param('insurance_module.module_insurance_analytics', self.module_insurance_analytics)
        self.env['ir.config_parameter'].sudo().set_param('insurance_module.module_vehicle_maintenance_reminder', self.module_vehicle_maintenance_reminder)
        self.env['ir.config_parameter'].sudo().set_param('insurance_module.module_safety_training_management', self.module_safety_training_management)

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            module_auto_inspection_reminder=self.env['ir.config_parameter'].sudo().get_param('insurance_module.module_auto_inspection_reminder', default=False),
            module_safety_dashboard=self.env['ir.config_parameter'].sudo().get_param('insurance_module.module_safety_dashboard', default=False),
            module_insurance_claim_automation=self.env['ir.config_parameter'].sudo().get_param('insurance_module.module_insurance_claim_automation', default=False),
            module_insurance_analytics=self.env['ir.config_parameter'].sudo().get_param('insurance_module.module_insurance_analytics', default=False),
            module_vehicle_maintenance_reminder=self.env['ir.config_parameter'].sudo().get_param('insurance_module.module_vehicle_maintenance_reminder', default=False),
            module_safety_training_management=self.env['ir.config_parameter'].sudo().get_param('insurance_module.module_safety_training_management', default=False)
        )
        return res 