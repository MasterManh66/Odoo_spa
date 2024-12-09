from odoo import models , fields , api


class Product(models.Model):
    _inherit = "product.product"

    outgoing_quantity = fields.Float(string='Xuất hàng', compute='_compute_outgoing_quantity')
    incoming_quantity = fields.Float(string='Nhập hàng', compute='_compute_incoming_quantity')

    @api.depends('stock_move_ids.product_qty', 'stock_move_ids.state', 'stock_move_ids.quantity')
    @api.depends_context('warehouse')
    def _compute_incoming_quantity(self):
        warehouse_id = self.env.context.get('warehouse')
        products = self.filtered(lambda x: x.type == 'product')
        for r in products:
            domain = [('product_id', '=', r.id),('state','=','done'),
                      ('picking_code', '=', 'incoming')
                      ]
            if warehouse_id:
                domain.append(('location_dest_id.warehouse_id.id', '=', warehouse_id))
            Moves = self.env['stock.move'].search(domain)
            r.incoming_quantity = sum(Moves.mapped('quantity'))

        services = self.filtered(lambda x: x.type == 'service')
        services.incoming_quantity = 0

    @api.depends('stock_move_ids.product_qty', 'stock_move_ids.state', 'stock_move_ids.quantity')
    @api.depends_context('warehouse')
    def _compute_outgoing_quantity(self):
        warehouse_id = self.env.context.get('warehouse')
        products = self.filtered(lambda x: x.type == 'product')
        for r in products:
            domain = [('product_id', '=', r.id), ('state', '=', 'done'),
                      ('picking_code', '=', 'outgoing')
                      ]
            if warehouse_id:
                domain.append(('location_id.warehouse_id.id', '=', warehouse_id))
            Moves = self.env['stock.move'].search(domain)
            r.outgoing_quantity = sum(Moves.mapped('quantity'))

        services = self.filtered(lambda x: x.type == 'service')
        services.outgoing_quantity = 0