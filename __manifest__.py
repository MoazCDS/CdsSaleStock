# -*- coding: utf-8 -*-
{
    'name': "CDS Sale Stock",
    'summary': """
    """,
    'description': """
    """,
    'author': "CDS Solutions SRL",
    'website': "www.cdsegypt.com",
    'contributors': [
        'Ramadan Khalil <rkhalil1990@gmail.com>',
    ],
    'version': '0.1',
    'depends': ["base", "sale", "sale_stock", "stock", "account", "web"],
    'data': [
        "security/groups.xml",
        "security/ir_rules.xml",
        "security/ir.model.access.csv",
        "views/menuitems.xml",
        "views/sale_training_tag_view.xml",
        "views/sale_order_view.xml",
        "views/account_move_view.xml",
        "reports/report_sale_order_training.xml",
        "wizard/sale_excel_export_view.xml",
    ],
    'license': 'OPL-1',
    "pre_init_hook": None,
    "post_init_hook": None,
}