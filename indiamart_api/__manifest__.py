# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "IndiaMART API",
    'icon': '/indiamart_api/static/description/icon.png',
    'summary': "IndiaMART API for integeration with CRM",
    'category': 'Services',
    'sequence': 170,
    'version': '1.200',
    'depends': ['crm'],
    'data': ['views/indiamartapi.xml','views/source.xml','views/settings.xml','data/cron.xml','security/ir.model.access.csv'],
    'application': True,
    'installable': True,
    'autoinstall': True,
    'assets': {
        'web.assets_backend': [],
        'web.assets_frontend': [],
    },
    'license': 'OEEL-1',
}
