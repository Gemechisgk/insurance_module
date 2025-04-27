{
    'name': 'Safety Health and Insurance',
    'version': '18.0.1.0.0',
    'category': 'Human Resources/Insurance',
    'summary': 'Manage office inspections, incident reporting, and insurance claims',
    'description': """
        This module provides comprehensive features for managing:
        - Office inspection management
        - Incident reporting
        - Fire extinguisher tracking
        - Vehicle inspection records
        - Insurance claims management
        - Employee safety suggestions
        - Accident investigation
    """,
    'author': 'Odoo',
    'website': 'https://www.odoo.com',
    'depends': [
        'base',
        'mail',
        'hr',
        'survey',
        'fleet',
        'web',
    ],
    'data': [
        # Security Groups first (no model dependencies)
        'security/insurance_security.xml',
        # Data files next
        'data/ir_sequence_data.xml',
        # Access rights (after models are loaded)
        'security/ir.model.access.csv',
        # Record rules (after models are loaded)
        'security/insurance_record_rules.xml',
        # Views and actions before menus
        'views/res_partner_views.xml',  # Partner views before other views
        'views/office_inspection_views.xml',
        'views/incident_report_views.xml',
        'views/fire_extinguisher_views.xml',
        'views/vehicle_inspection_views.xml',
        'views/insurance_claim_views.xml',
        'views/insurance_type_views.xml',
        'views/employee_suggestion_views.xml',
        'views/accident_investigation_views.xml',
        'views/res_config_settings_views.xml',
        # Menu last (after all views and actions are loaded)
        'views/menu_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'post_init_hook': 'post_init_hook',
} 