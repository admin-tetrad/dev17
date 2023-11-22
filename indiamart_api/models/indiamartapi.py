import requests
import json
from odoo import api, fields, models
from datetime import datetime, timedelta
from typing import List, Dict, Any

class Crmlead(models.Model):
    _inherit = ['crm.lead']
    x_studio_unique_query_id = fields.Char(string="Unique Query ID")
    x_studio_unique_query_time = fields.Datetime(string="Unique Query Time")
    
    def create_records(self, current_date):
        settings = self.env['res.config.settings'].sudo().get_values()
        api_key = settings['IndiaMART_API_KEY']
        url = 'https://mapi.indiamart.com/wservce/crm/crmListing/v2/?glusr_crm_key={}&start_time={}&end_time={}'.format(api_key,current_date, current_date)
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)

            if data.get('CODE') == 200 and data.get('STATUS') == 'SUCCESS':
                records = data.get('RESPONSE', [])
                country_codes = self.search_country_name(records)
                state_id = self.search_state_name(records)
                query_time = self.format_query_time(records)
                for i, record in enumerate(records):
                    lead = self.env['unique.query.source'].search([('name', '=', record.get('UNIQUE_QUERY_ID'))])
                    self.env['unique.query.source'].create({
                        'name': record.get('UNIQUE_QUERY_ID'
                                           )})
                    if not lead:
                        address = record.get('SENDER_ADDRESS')
                        if address:
                            address_parts = record.get('SENDER_ADDRESS').split(',')
                            street = address_parts[0].strip()
                            street2 = ','.join(address_parts[1:-2]).strip()
                            pin_code = address_parts[-1].strip() if address_parts[-1][-6:].isdigit() else ""
                        else:
                            street = ''
                            street2 = ''
                            pin_code = ''

                        self.env['crm.lead'].create({
                            'x_studio_unique_query_id': record.get('UNIQUE_QUERY_ID'),
                            'x_studio_unique_query_time': query_time[i],
                            'contact_name': record.get('SENDER_NAME'),
                            'email_from': record.get('SENDER_EMAIL'),
                            'name': record.get('SUBJECT'),
                            'partner_name': record.get('SENDER_COMPANY'),
                            'street': record.get('SENDER_ADDRESS'),
                            'street': street,
                            'street2': street2,
                            'city': record.get('SENDER_CITY'),
                            'zip': pin_code,
                            'state_id': state_id[i],
                            'country_id': country_codes[i],
                            'mobile': record.get('SENDER_MOBILE'),
                            'description': record.get('QUERY_MESSAGE'),
                            'source_id': self.search_utm_source().id,
                        })
            else:
                raise ValueError(f"Failed to fetch data. CODE: {data.get('CODE')}, STATUS: {data.get('STATUS')}")
        else:
            raise ValueError(f"Failed to fetch data. Response code: {response.status_code}")

        
    @api.model
    def create_records_yesterday(self):
        current_date = fields.Date.today() - timedelta(days=1)
        current_date_str = current_date.strftime('%d-%b-%Y')
        self.create_records(current_date_str)
    
    @api.model
    def create_records_today(self):
        current_date = fields.Date.today()
        current_date_str = current_date.strftime('%d-%b-%Y')
        self.create_records(current_date_str)
    
    def search_country_name(self, records):
        country_codes = []
        for record in records:
            sender_country_iso = record.get('SENDER_COUNTRY_ISO')
            country = self.env['res.country'].search([('code', '=', sender_country_iso)])
            if country:
                country_codes.append(country.id)
            else:
                country_codes.append(None)
        return country_codes
    
    def format_query_time(self, records):
        query_times = []
        for record in records:
            sender_query_time = record.get('QUERY_TIME')
            query_time = (datetime.strptime(sender_query_time, '%Y-%m-%d %H:%M:%S') - timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M:%S')
            query_times.append(query_time)
        return query_times
    
    def search_state_name(self, records):
        state_id = []
        for record in records:
            sender_state = record.get('SENDER_STATE')
            state = self.env['res.country.state'].search([('name', '=', sender_state)])
            if state:
                state_id.append(state.id)
            else:
                state_id.append(None)
        return state_id
    
    def search_utm_source(self):
        utm = self.env['utm.source'].search([('name', 'ilike', 'IndiaMART')], limit=1)
        if utm:
            return utm
        else:
            return self.env['utm.source'].create({'name': 'IndiaMART'})