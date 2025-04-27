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