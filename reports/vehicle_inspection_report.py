from odoo import models, fields, api, _

class VehicleInspectionReport(models.AbstractModel):
    _name = 'report.insurance_module.report_vehicle_inspection'
    _description = 'Vehicle Inspection Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['vehicle.inspection'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'vehicle.inspection',
            'docs': docs,
            'data': data,
            'get_status_display': self._get_status_display,
            'get_checkbox': self._get_checkbox,
        }

    def _get_status_display(self, status):
        """Helper method to get display value for status fields"""
        status_map = {
            'ok': 'OK',
            'defective': 'Defective',
            'missing': 'Missing',
            'fade': 'Fade-out',
        }
        return status_map.get(status, status)

    def _get_checkbox(self, value, status):
        """Helper method to generate checkbox HTML"""
        if value == status:
            return '[✓]'
        return '[ ]' 