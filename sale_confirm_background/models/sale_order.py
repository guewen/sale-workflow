# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.addons.queue_job.job import job


class Sale(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(
        selection_add=[('confirm_background', 'Confirm in Background')]
    )

    @job(default_channel='root.background.sale_confirm')
    @api.multi
    def confirm_in_background(self, notify=True):
        """Confirm sales order in background"""
        self.ensure_one()
        if self.state != 'confirm_background':
            return
        self.action_confirm()
        if notify:
            action = self.env.ref('sale.action_orders').read()[0]
            action.update({
                'res_id': self.id,
                'views': [(False, 'form')],
            })
            self.env.user.notify_info(
                _('Order %s is now confirmed.') % self.name,
                sticky=True,
                action=action,
            )

    def action_confirm_background(self):
        # compatibility with sale_exception
        # we want to raise interactively, not in background
        if self.detect_exceptions():
            return self._popup_exceptions()
        self.write({
            'state': 'confirm_background',
            'confirmation_date': fields.Datetime.now(),
        })
        for order in self:
            self.env.user.notify_info(
                _('Order %s will be confirmed in background.') % order.name,
            )
            order.with_delay(
                description=_(
                    'Confirmation of sales order %s'
                ) % order.name,
            ).confirm_in_background(notify=False)
