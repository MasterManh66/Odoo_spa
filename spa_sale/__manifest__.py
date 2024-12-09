# -*- coding: utf-8 -*-
{
    'license': 'LGPL-3',
    'name': "SPA Sale",
    'summary': "The custom sale",
    'author': '',
    'website': "",
    'support': '',
    'category': '',
    'version': '1.1',
    'depends': [
        'sale',
        'stock',
        'hr',
        # 'spa_regimen',
        'product',
        'loyalty',
        'sale_management',
        'report_xlsx'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/ir_sequence.xml',
        'views/sale_order_views.xml',
        'views/product_template.xml',
        'views/product_category.xml',
        'views/loyalty_program_views.xml',
        'views/res_partner.xml',
        'views/sale_menus.xml',
        'views/stock_quant.xml',
        'reports/revenue_report.xml',
        'wizards/revenue_pop.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'spa_sale/static/src/**/*',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}
