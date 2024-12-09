from odoo import api, fields, models
from odoo.osv import expression


class ResPartner(models.Model):
    _inherit = 'res.partner'


    @api.model
    def _name_search(self, name, domain=None, operator='ilike', limit=None, order=None):
        domain = domain or []
        context = self.env.context.get('search_customer', False)
        if context:
            domain = expression.AND([domain, [('is_customer', '=', True)]])
        return super()._name_search(name, domain, operator, limit, order)

    @api.model_create_multi
    def create(self, vals_list):
        category_id = self.env['res.partner.category'].search([('customer_type', '=', 'customer')], limit=1)
        for vals in vals_list:
            if self.env.context.get('default_category_type', False) == 'customer':
                vals['category_id'] = category_id.ids
        return super().create(vals_list)
