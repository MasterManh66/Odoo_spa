from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    location_id = fields.Many2one('stock.location', string="Kho bán")
    qty_inventory = fields.Float(string='Tồn kho', compute='_compute_inventory', digits='Product Unit of Measure')
    discount_employee = fields.Integer(string='Hoa hồng', compute='_compute_discount_employee')
    type_product_tmpl = fields.Selection(related='product_template_id.detailed_type')
    date_sale = fields.Date(string='Ngày bán')

    @api.onchange('product_template_id')
    def onchange_product_template_id(self):
        for r in self:
            r.price_unit = r.product_template_id.list_price

    @api.depends('product_template_id', 'product_id', 'location_id', 'product_uom')
    def _compute_inventory(self):
        for r in self:
            stock_quant_id = self.env['stock.quant'].search(
                [('product_id', '=', r.product_id.id), ('location_id', '=', r.location_id.id)])
            if stock_quant_id:
                if r.product_uom:
                    r.qty_inventory = stock_quant_id.product_uom_id._compute_quantity(stock_quant_id.inventory_quantity_auto_apply, r.product_uom)
                else:
                    r.qty_inventory = stock_quant_id.inventory_quantity_auto_apply
            else:
                r.qty_inventory = 0

    @api.constrains('product_template_id', 'location_id')
    def _check_product_template_location(self):
        for r in self:
            so_line_ids = self.env['sale.order.line'].search(
                [('product_template_id', '=', r.product_template_id.id), ('location_id', '=', r.location_id.id),
                 ('order_id', '=', r.order_id.id)])
            if len(so_line_ids) > 1:
                raise ValidationError(
                    'Không được chọn hai sản phẩm giống nhau và cùng kho trong cùng một đơn bán hàng.')

    @api.depends('product_template_id', 'price_subtotal')
    def _compute_discount_employee(self):
        for r in self:
            r.discount_employee = r.product_template_id.discount / 100 * r.price_subtotal if r.product_template_id.discount else 0
