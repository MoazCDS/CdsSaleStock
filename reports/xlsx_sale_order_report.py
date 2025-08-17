# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import io
import xlsxwriter
from ast import literal_eval

class XlsxSaleOrderReport(http.Controller):
    @http.route('/sale_order/excel/reports/<string:sale_order_ids>', type="http", auth="user")
    def download_sale_order_excel_report(self, sale_order_ids):

        sale_order_ids = request.env['sale.order'].browse(literal_eval(sale_order_ids))

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Sale Orders')

        headers = ['Order', 'Customer', 'Date', 'Total', 'Stock Ready', 'Tags', 'Status']
        header_format = workbook.add_format({"bold": True, 'bg_color': '#D3D3D3', 'border': 1, 'align': 'center'})
        left_align_format = workbook.add_format({'align': 'left'})
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, header_format)

        row_num = 1
        for order in sale_order_ids:
            worksheet.write(row_num, 0, order.name, left_align_format)
            worksheet.write(row_num, 1, order.partner_id.name, left_align_format)
            worksheet.write(row_num, 2, order.date_order, left_align_format)
            worksheet.write(row_num, 3, order.amount_total, left_align_format)
            worksheet.write(row_num, 4, "Yes" if order.stock_ready else "No", left_align_format)
            tags = ', '.join(order.training_tag_ids.mapped('name')) if order.training_tag_ids else '-'
            worksheet.write(row_num, 5, tags, left_align_format)
            worksheet.write(row_num, 6, order.state, left_align_format)
            row_num += 1

        workbook.close()
        output.seek(0)

        return request.make_response(
            output.read(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', 'attachment; filename="Sale Order Report.xlsx"')
            ]
        )