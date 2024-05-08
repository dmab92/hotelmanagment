# -*- coding:Utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class rapoort_expedition_parser(models.AbstractModel):
    _name = 'report.hotel_management_odoo.report_sale_order'
    _description = 'Rapport  des ventes'

    def _get_report_values(self, docids, data=None):
        domain = []
        total_sortie=0
        if data.get('checkin_date'):
            domain.append(('date_order', '>=', data.get('checkin_date')))
        if data.get('checkout_date'):
            domain.append(('date_order', '<=', data.get('checkout_date')))

        docs = self.env['room.booking'].search(domain, order="date_order desc")
        sorties = self.env['purchase.order'].search(domain)
        #total_sortie += sum(sorties.mapped('price_total'))
        #total_sortie += sum(sorties.mapped('price_subtotal'))
        #for record in sorties:
        total_sortie= sum(line.price_subtotal for line in sorties)

        return {
            'doc_ids': docs.ids,
            'doc_model': 'room.booking',
            'docs': docs,
            'datas': data,
            'sorties':sorties,
            'total_sortie':total_sortie

        }

