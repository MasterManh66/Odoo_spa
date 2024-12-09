from odoo import api, fields, models
from odoo.osv import expression


class ProductCategory(models.Model):
    _inherit = 'product.category'

    type = fields.Selection([('service', 'Dịch vụ'), ('product', 'Sản phẩm')], string='Loại danh mục')

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        domain = domain or []
        context = self.env.context.get('default_type', False)
        if context and not self:
            if context == 'service':
                domain = expression.AND([domain, [('type', '=', 'service')]])
            if context == 'product':
                domain = expression.AND([domain, [('type', '=', 'product')]])
        return super()._search(domain, offset, limit, order, access_rights_uid)
