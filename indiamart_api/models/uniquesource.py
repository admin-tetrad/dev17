from odoo import fields, models,api, _


class uniquequerysource(models.Model):
    _name = "unique.query.source"
    _description = 'unique query source'

    name = fields.Char('Unique Query Store', required=True, translate=True)

@api.model
def copy_field_value(self, records):
    self.env.create({'name': record.get('UNIQUE_QUERY_ID')} for record in records)