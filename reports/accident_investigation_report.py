from odoo import models, fields, api

class AccidentInvestigationReport(models.AbstractModel):
    _name = 'report.insurance_module.accident_investigation_report'
    _description = 'Accident Investigation Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['accident.investigation'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'accident.investigation',
            'docs': docs,
            'data': data,
        } 