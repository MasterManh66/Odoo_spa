from odoo import api, fields, models


class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'model' in vals and ['model'] == 'res.partner':
                res_partner_id = self.env['res.partner'].browse(vals['res_id'])
                if res_partner_id.is_customer:
                    vals['body'] = 'Khách hàng đã được tạo.'
                if res_partner_id.is_supplier:
                    vals['body'] = 'Nhà cung cấp đã được tạo.'
        recs = super(MailMessage, self).create(vals_list)
        return recs
