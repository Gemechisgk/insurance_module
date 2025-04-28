from odoo import models, fields, api

class IncidentReport(models.AbstractModel):
    _name = 'report.insurance_module.incident_report'
    _description = 'Incident Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['incident.report'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'incident.report',
            'docs': docs,
            'data': data,
        } 