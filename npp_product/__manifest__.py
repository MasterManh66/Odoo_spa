# -*- coding: utf-8 -*-
{
    'license': 'LGPL-3',
    'name': "SPA Product",
    'summary': "The custom product",
    'author': '',
    'website': "",
    'support': '',
    'category': '',
    'version': '1.1',
    'depends': [
        'product',
        'stock',
        'sale_product_configurator'
    ],
    'data': [
        'views/product_template.xml',
        'views/product_view.xml',
    ],

    'assets': {
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}
