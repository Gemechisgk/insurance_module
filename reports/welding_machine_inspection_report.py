from odoo import models, api

class WeldingMachineInspectionReport(models.AbstractModel):
    _name = 'report.insurance_module.welding_machine_inspection_report'
    _description = 'Welding Machine Inspection Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['welding.machine.inspection'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'welding.machine.inspection',
            'docs': docs,
            'data': data,
        } 