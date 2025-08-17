# -*- coding: utf-8 -*-

##############################################################################
#    Copyright (c) 2021 CODOOS SRL. (http://codoos.com)
#    Maintainer: Eng.Ramadan Khalil (<rkhalil1990@gmail.com>)
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
##############################################################################

from odoo import models, fields


class SaleExcelExportWizard(models.TransientModel):
    _name = 'sale.excel.wizard'

    salesperson = fields.Many2one('res.users')
    date_from = fields.Date()
    date_to = fields.Date()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ('any', 'Any'),
    ], default='any')

    def export_with_filter_action(self):
        for rec in self:
            domain = []
            if rec.date_from:
                dt_from = fields.Datetime.to_datetime(rec.date_from)
                domain.append(('date_order', '>=', fields.Datetime.to_string(dt_from)))
            if rec.date_to:
                dt_to = fields.Datetime.to_datetime(rec.date_to)
                domain.append(('date_order', '<=', fields.Datetime.to_string(dt_to)))
            if rec.state and rec.state != 'any':
                domain.append(('state', '=', rec.state))
            if rec.salesperson:
                domain.append(('user_id', '=', rec.salesperson.id))

            records = self.env['sale.order'].search(domain)

            return {
                'type': 'ir.actions.act_url',
                'url': f"/sale_order/excel/reports/{str(records.ids)}",
                'target': 'new',
            }
