from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def default_get(self, fields):
        res = super(ProductTemplate, self).default_get(fields)
        if 'detailed_type' in fields:
            res['available_in_pos'] = True
        return res
