from odoo import api, fields, models, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    price_purchase = fields.Float(string='Giá mua', digits='Product Price', tracking=True)
    price_purchase_per_uom = fields.Float(string='Giá bán/buổi', digits='Product Unit of Measure', tracking=True)
    overtime_discount = fields.Float('Hoa hồng ngoài giờ', digits='Product Unit of Measure', tracking=True)
    hourly_discount = fields.Float('Hoa hồng trong giờ', digits='Product Unit of Measure', tracking=True)
    discount = fields.Float('Hoa hồng', tracking=True)
    regimen_count = fields.Integer('Số buổi liệu trình', default=1, tracking=True)
    duration = fields.Integer(string='Thời lượng (phút)', tracking=True)
    regimen_donate = fields.Integer(string='Số buổi tặng', default=0, tracking=True)
    list_price = fields.Float(
        'Giá bán', default=1.0,
        digits='Product Price', tracking=True,
        help="Price at which the product is sold to customers.",
    )
    categ_id = fields.Many2one(
        'product.category', 'Product Category',
        change_default=True,
        default=lambda self: self.env['product.template']._get_default_category_id(),
        group_expand='_read_group_categ_id',
        required=True,
        tracking=True
        )
    order_sold = fields.Integer(compute="_compute_sale_order")
    guarantee_time = fields.Integer(string='Bảo hành')

    def _compute_sale_order(self):
        for l in self:
            l.order_sold = self.env['sale.order.line'].search_count([('product_template_id', '=', l.id)]) or 0
            
    def get_formview_id(self, access_uid=None):
        if self.detailed_type == 'service':
            return self.env.ref('spa_sale.product_template_service_form_view').id
        else:
            return self.env.ref('spa_sale.product_template_consu_form_view_inherit').id

    # @api.depends('regimen_count', 'list_price')
    # def _compute_price_per_uom(self):
    #     for r in self:
    #         if r.regimen_count:
    #             r.price_purchase_per_uom = r.list_price/r.regimen_count
    #         else:
    #             r.price_purchase_per_uom = 0

    def _creation_message(self):
        if self.detailed_type == 'service' and self.env.context['lang'] == 'vi_VN':
            return ("Dịch vụ đã được tạo")
        return super()._creation_message()

    @api.model
    def default_get(self, fields):
        res = super(ProductTemplate, self).default_get(fields)
        res['list_price'] = 0
        return res
    
    def action_list_sale_sold(self):
        sols = self.env['sale.order.line'].search([('product_template_id', '=', self.id)])
        sale_order_ids = [l.order_id.id for l in sols]
        action = self.env['ir.actions.actions']._for_xml_id('sale.action_quotations_with_onboarding')
        action['name'] = _('Đã bán')
        action['domain'] = [('id', 'in', sale_order_ids)]
        action['target'] = 'current'
        
        if not isinstance(action.get('context'), dict):
            action['context'] = {}
        action['context']['search_default_my_quotation'] = 0
        
        return action