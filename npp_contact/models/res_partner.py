# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re
from odoo.osv import expression


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def default_country_ids(self):
        country_id = self.env.ref('base.vn')
        return country_id

    is_customer = fields.Boolean(string="Là khách hàng", default=False)
    is_supplier = fields.Boolean(string="Là nhà cung cấp", default=False)
    country_id = fields.Many2one(default=default_country_ids)

    @api.depends('category_id', 'category_id.customer_type')
    def _compute_customer_type(self):
        for partner in self:
            customer_types = partner.category_id.mapped('customer_type')
            partner.is_customer = 'customer' in customer_types if customer_types else False
            partner.is_supplier = 'supplier' in customer_types if customer_types else False

    @api.constrains('phone', 'mobile', 'email')
    def _check_phone(self):
        for r in self:
            number = r'^\d{10,12}$'
            email = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
            if r.mobile and r.phone and r.mobile == r.phone:
                raise ValidationError('Số điện thoại và di dộng không được trùng nhau.')
            if r.phone and not re.match(number, r.phone):
                raise ValidationError("Số điện thoại không hợp lệ.")
            if r.mobile and not re.match(number, r.mobile):
                raise ValidationError("Số di động không hợp lệ.")
            if r.email and not re.match(email, r.email):
                raise ValidationError("Email không hợp lệ.")
            if r.phone:
                self.validate_phone(r.phone, 'điện thoại')
            if r.mobile:
                self.validate_phone(r.mobile, 'di động')
            if r.email:
                partner_email_ids = self.env['res.partner'].search([('email', '=', r.email)])
                if len(partner_email_ids) > 1:
                    raise ValidationError('Email đã tồn tại.')

    def validate_phone(self, phone, type_phone):
        partner_phone_ids = self.env['res.partner'].search([('phone', '=', phone)])
        partner_mobile_ids = self.env['res.partner'].search([('mobile', '=', phone)])
        if len(partner_phone_ids) > 1 or len(partner_mobile_ids) > 1:
            raise ValidationError('Số %s đã tồn tại trên hệ thống.' % type_phone)
        return True

    @api.model
    def _name_search(self, name, domain=None, operator='ilike', limit=None, order=None):
        domain = domain or []
        if name:
            domain_search = ['|', '|', ('name', operator, name), ('phone', operator, name),
                             ('mobile', operator, name)]
            domain = expression.AND([domain, domain_search])
        return self._search(domain, limit=limit, order=order)
