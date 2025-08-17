# -*- coding: utf-8 -*-

##############################################################################
#    Copyright (c) 2021 CODOOS SRL. (http://codoos.com)
#    Maintainer: Eng.Ramadan Khalil (<rkhalil1990@gmail.com>)
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    training_tag_ids = fields.Many2many("sale.training.tag","sale_order_training_tag_rel",
        "order_id", "tag_id", string="Training Tags",)
    stock_ready = fields.Boolean(compute='_compute_stock_ready', store=True)
    customer_note = fields.Text()

    @api.depends('order_line.product_id', 'order_line.product_uom_qty', 'order_line.product_uom', 'warehouse_id')
    def _compute_stock_ready(self):
        Quant = self.env['stock.quant']
        for order in self:
            ready = True
            wh = order.warehouse_id
            if not wh:
                order.stock_ready = False
                continue

            source_loc = wh.lot_stock_id
            relevant_lines = order.order_line.filtered(
                lambda l: l.product_id and l.product_id.type == 'product' and not l.display_type
            )
            if not relevant_lines:
                order.stock_ready = False
                continue

            for line in relevant_lines:
                product = line.product_id
                on_hand = Quant._get_available_quantity(product, source_loc)
                on_hand_in_line_uom = product.uom_id._compute_quantity(on_hand, line.product_uom)
                if on_hand_in_line_uom < line.product_uom_qty:
                    ready = False
                    break

            order.stock_ready = ready

    def action_confirm(self):
        trainee = self.env.user.has_group('cds_sale_stock.sales_trainee_group')
        supervisor = self.env.user.has_group('cds_sale_stock.sales_supervisor_group')
        if trainee and not supervisor and not self.stock_ready:
            raise UserError(_("Caon't confirm the order, Please ask a supervisor"))
        return super().action_confirm()

    def _prepare_invoice(self):
        vals = super()._prepare_invoice()
        if self.customer_note:
            vals['customer_notes'] = self.customer_note
        return vals

    def action_export_with_filter(self):
        action = self.env['ir.actions.actions']._for_xml_id("cds_sale_stock.sale_excel_wizard_action")
        # action['context'] = {'default_timesheet_id': self.id}
        return action