# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Confirmed in Background',
    'version': '10.0.1.0.0',
    'author': 'Camptocamp',
    'license': 'AGPL-3',
    'category': 'Sales',
    'depends': [
        'sale',
        'queue_job',
        'web_notify',
        'sale_exception',
    ],
    'website': 'https://www.camptocamp.com',
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
}
