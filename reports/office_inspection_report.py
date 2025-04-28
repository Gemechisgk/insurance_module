from odoo import models, fields, api

class OfficeInspectionReport(models.AbstractModel):
    _name = 'report.insurance_module.office_inspection_report'
    _description = 'Office Inspection Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['office.inspection'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'office.inspection',
            'docs': docs,
            'data': data,
        } 