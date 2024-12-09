# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ResPartnerCategory(models.Model):
    _inherit = 'res.partner.category'

    customer_type = fields.Selection(string="Loại khách hàng",
                                     selection=[('customer', 'Khách hàng'), ('supplier', 'Nhà cung cấp')], default='customer')

