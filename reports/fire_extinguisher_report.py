from odoo import models, fields, api

class FireExtinguisherReport(models.AbstractModel):
    _name = 'report.insurance_module.fire_extinguisher_report'
    _description = 'Fire Extinguisher Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['fire.extinguisher'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'fire.extinguisher',
            'docs': docs,
            'data': data,
        } 