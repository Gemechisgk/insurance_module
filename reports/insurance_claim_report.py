from odoo import models, fields, api

class InsuranceClaimReport(models.AbstractModel):
    _name = 'report.insurance_module.insurance_claim_report'
    _description = 'Insurance Claim Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['insurance.claim'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'insurance.claim',
            'docs': docs,
            'data': data,
        } 