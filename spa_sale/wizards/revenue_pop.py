from odoo import api, fields, models

from odoo.exceptions import ValidationError


class RevenuePop(models.TransientModel):
    _name = 'revenue.pop'
    date_start = fields.Date(string='Ngày bắt đầu', required=True)
    date_end = fields.Date(string='Ngày kết thúc', required=True)
    type = fields.Selection([('product', 'Sản phẩm'), ('service', 'Dịch vụ')], string='Loại sản phẩm')

    def action_done(self):
        self.ensure_one()
        report_action = self.env.ref('spa_sale.report_revenue_report').report_action(self)
        report_action['close_on_report_download'] = True
        return report_action

    @api.constrains('date_start', 'date_end')
    def _check_date_end(self):
        if self.date_end < self.date_start:
            raise ValidationError('Ngày kết thúc không được nhỏ hơn ngày bắt đầu')