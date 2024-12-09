# -*- coding: utf-8 -*-
{
    'license': 'LGPL-3',
    'name': "SPA Contact",
    'summary': "The custom contact",
    'author': '',
    'website': "",
    'support': '',
    'category': '',
    'version': '1.1',
    'depends': [
        'contacts',
        'account',
        'base_geolocalize',
        'sale',
        'purchase_stock',
        'crm',
        'calendar'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner.xml',
        'views/res_partner_category.xml',
    ],

    'assets': {
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}