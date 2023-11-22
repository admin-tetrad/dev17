from odoo import fields, models

class ResConfigSettingsInherit(models.TransientModel):
    _inherit = 'res.config.settings'

    IndiaMART_API_KEY = fields.Char(string='IndiaMART_API_KEY')

    def set_values(self):
        res = super(ResConfigSettingsInherit, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('crm_lead.IndiaMART_API_KEY', self.IndiaMART_API_KEY)
        return res

    def get_values(self):
        res = super(ResConfigSettingsInherit, self).get_values()
        IndiaMART_API_KEY = self.env['ir.config_parameter'].sudo().get_param('crm_lead.IndiaMART_API_KEY', default=False)
        res.update(
            IndiaMART_API_KEY=IndiaMART_API_KEY
        )
        return res
