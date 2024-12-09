from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            picking_type_id = self.env['stock.picking.type'].browse(val.get('picking_type_id'))
            context = self.env.context.get('pass_context', False) or self.env.context.get('search_default_my_quotation', False)
            if picking_type_id.code == 'outgoing':
                so_line_id = self.env['sale.order.line'].browse(val.get('sale_line_id'))
                if so_line_id and so_line_id.product_template_id.detailed_type == 'product':
                    val['location_id'] = so_line_id.location_id.id or picking_type_id.default_location_src_id.id
        recs = super(StockMove, self).create(vals_list)
        return recs
