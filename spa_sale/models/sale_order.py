from datetime import timedelta, datetime
import pytz
from odoo import api, fields, models, _

from odoo.exceptions import ValidationError, UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _default_sale_employee_id(self):
        return self.env.user.employee_id if self.env.user.employee_id else None

    employee_sale_id = fields.Many2one('hr.employee', string='Nhân viên bán hàng',default=_default_sale_employee_id)
    technicians_id = fields.Many2one('hr.employee', string='Kỹ thuật viên')
    email_partner = fields.Char(string='Email')
    mobile_partner = fields.Char(string='Điện thoại')

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        for r in self:
            if r.partner_id:
                r.email_partner = r.partner_id.email
                r.mobile_partner = r.partner_id.mobile or r.partner_id.phone


    def _show_cancel_wizard(self):
        return False

    # def action_confirm(self):
    #     for r in self:
    #         if len(r.order_line) <= 0:
    #             raise ValidationError('Bạn chưa nhập thông tin chi tiết đơn hàng.')
    #         for line in r.order_line:
    #             line.date_sale = fields.Date.today()
    #             if line.product_uom_qty <= 0:
    #                 raise ValidationError('Số lượng sản phẩm phải lớn hơn 0.')
    #             if line.qty_inventory < line.product_uom_qty and line.product_template_id.detailed_type == 'product':
    #                 raise ValidationError('Sản phẩm %s không đủ trong kho.' % line.product_template_id.name)
    #     self.picking_ids.button_validate()
    #     res = super().action_confirm()
    #     return res

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            val['name'] = self.env['ir.sequence'].next_by_code('sale.order.customize')
        recs = super(SaleOrder, self).create(vals_list)
        return recs
