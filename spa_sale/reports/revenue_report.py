from odoo import api, fields, models
import base64
from io import BytesIO


class RevenueReport(models.TransientModel):
    _name = 'report.report_revenue_report'
    _description = 'Báo cáo doanh thu'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, records):
        ws = workbook.add_worksheet('Báo cáo doanh thu')
        
        font_name = 'Times New Roman'
        left_bold = workbook.add_format({'text_wrap': 0, 'align': 'left', 'valign': 'vcenter', 'font_name': font_name, 'font_size': 12, 'bold': 1})
        left_bold_header = workbook.add_format({'text_wrap': 1, 'align': 'left', 'valign': 'bottom', 'font_name': font_name, 'font_size': 16, 'bold': 1})
        left_bold_title = workbook.add_format({'text_wrap': 1, 'align': 'center', 'valign': 'vcenter', 'font_name': font_name, 'font_size': 14, 'bold': 1})
        content_center = workbook.add_format({'text_wrap': 1, 'align': 'center', 'valign': 'vcenter', 'font_name': font_name, 'font_size': 12, 'border': 1, 'bold': 0})
        content_center_header = workbook.add_format({'text_wrap': 1, 'align': 'center', 'valign': 'vcenter', 'font_name': font_name, 'font_size': 12, 'bold': 0})
        content_right = workbook.add_format({'text_wrap': 1, 'align': 'right', 'valign': 'vcenter', 'font_name': font_name, 'font_size': 12, 'border': 1, 'bold': 0})
        content_right_bole = workbook.add_format({'text_wrap': 1, 'align': 'right', 'valign': 'vcenter', 'font_name': font_name, 'border': 1, 'bold': 1})
        content_left = workbook.add_format({'text_wrap': 1, 'align': 'left', 'valign': 'vcenter', 'font_name': font_name, 'font_size': 12, 'border': 1, 'bold': 0})
        center_bold = workbook.add_format({'bold': 1, 'text_wrap': 1, 'align': 'center', 'valign': 'vcenter', 'font_name': font_name, 'border': 1, 'font_size': 12, 'bg_color': '#F8CBAD'})
        
        row = 0
        company = self.env.user.company_id
        if company.logo:
            logo = BytesIO(base64.b64decode(company.logo))
            ws.insert_image(row, 0, 'checkbox.png', {
                'image_data': logo,
                'x_offset': 0.1,
                'y_offset': 0.1,
                'x_scale': 0.48,
                'y_scale': 0.39
            })
        ws.merge_range(row, 2, row + 1, 11, self.env.user.company_id.name, left_bold_header)

        row += 2
        ws.merge_range(row, 2, row + 1, 11, self.env.user.company_id.partner_id._display_address(without_company=True),
                       left_bold)
        row += 3
        ws.merge_range(row, 0, row, 11, 'BÁO CÁO DOANH THU', left_bold_title)

        row += 1
        ws.merge_range(row, 0, row, 11, '(Từ ngày %s đến ngày %s)' % (
            records.date_start.strftime('%d-%m-%Y'), records.date_end.strftime('%d-%m-%Y')), content_center_header)
        ws.set_column(0, 0, 10)
        ws.set_column(1, 1, 20)
        ws.set_column(2, 2, 30)
        ws.set_column(3, 3, 20)
        ws.set_column(4, 4, 30)
        ws.set_column(5, 5, 20)
        ws.set_column(6, 6, 20)
        ws.set_column(7, 7, 20)
        ws.set_column(8, 8, 20)
        ws.set_column(9, 9, 20)
        ws.set_column(10, 10, 20)

        row += 2
        ws.write(row, 0, 'STT', center_bold)
        ws.write(row, 1, 'Ngày bán hàng', center_bold)
        ws.write(row, 2, 'Tên khách hàng', center_bold)
        ws.write(row, 3, 'Đơn bán hàng', center_bold)
        ws.write(row, 4, 'Tên sản phẩm', center_bold)
        ws.write(row, 5, 'Số lượng', center_bold)
        ws.write(row, 6, 'Đơn giá', center_bold)
        ws.write(row, 7, 'Chiết khấu', center_bold)
        ws.write(row, 8, 'Tiền trước thuế', center_bold)
        ws.write(row, 9, 'Thuế', center_bold)
        ws.write(row, 10, 'Tiền sau thuế', center_bold)
        domain = ''
        if records.type:
            domain = "and pt.detailed_type = '%s'" % records.type
        else:
            domain = 'and 1=1'
        sql = f'''
            select 
                rp.name as ten_khach_hang, 
                so.name as don_ban_hang, 
                so.date_order as date_order, 
                pt.name as ten_sp,
                sol.product_uom_qty as so_luong,
                sol.price_unit as don_gia,
                sol.price_subtotal as tien_truoc_thue,
                sol.price_tax as thue,
                sol.price_total as gia_tien,
                sol.date_sale,
                sol.discount as chiet_khau 
            from sale_order_line sol 
            left join sale_order so on sol.order_id = so.id
            left join res_partner rp on rp.id = so.partner_id 
            left join product_product pp on sol.product_id = pp.id
            left join product_template pt on pt.id = pp.product_tmpl_id 
            where so.state = 'sale' 
                and so.date_order::date between '{records.date_start}' 
                and '{records.date_end}' 
                {domain}
        '''
        self._cr.execute(sql)
        res = self._cr.dictfetchall()
        row += 1
        stt = 1
        price_discount = 0
        price_subtotal = 0
        price_tax = 0
        price_total = 0
        for r in res:
            
            ws.write(row, 0, stt, content_center)
            ws.write(row, 1, r.get('date_order', '').strftime('%d-%m-%Y'), content_center)
            ws.write(row, 2, r.get('ten_khach_hang', ''), content_left)
            ws.write(row, 3, r.get('don_ban_hang', ''), content_center)
            ws.write(row, 4, r.get('ten_sp').get('vi_VN') if r.get('ten_sp').get('vi_VN') else r.get('ten_sp').get('en_US'), content_left)
            ws.write(row, 5, '{:,}'.format(int(r.get('so_luong', 0))), content_right)
            ws.write(row, 6, '{:,}'.format(int(r.get('don_gia', 0))), content_right)
            
            ws.write(row, 7, '{:,}'.format(int(int(r.get('so_luong', 0)) * int(r.get('don_gia', 0)) * int(r.get('chiet_khau', 0)) / 100)), content_right)
            ws.write(row, 8, '{:,}'.format(int(r.get('tien_truoc_thue', 0))), content_right)
            ws.write(row, 9, '{:,}'.format(int(r.get('thue', 0))), content_right)
            ws.write(row, 10, '{:,}'.format(int(r.get('gia_tien', 0))), content_right)
            price_discount += int(int(r.get('so_luong', 0)) * int(r.get('don_gia', 0)) * int(r.get('chiet_khau', 0)) / 100)
            price_subtotal += int(r.get('tien_truoc_thue', 0))
            price_tax += int(r.get('thue', 0))
            price_total += int(r.get('gia_tien', 0))
            row += 1
            stt += 1
        row += 1
        ws.write(row, 7, '{:,}'.format(price_discount), content_right_bole)
        ws.write(row, 8, '{:,}'.format(price_subtotal), content_right_bole)
        ws.write(row, 9, '{:,}'.format(price_tax), content_right_bole)
        ws.write(row, 10, '{:,}'.format(price_total), content_right_bole)
