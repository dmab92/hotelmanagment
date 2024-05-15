# -*- coding:Utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class rapoort_expedition_parser(models.AbstractModel):
    _name = 'report.hotel_management_odoo.report_sale_order'
    _description = 'Rapport  des ventes'

    def _get_report_values(self, docids, data=None):
        domain = []
        domain_5k = []
        nb_5k= 0
        nb_7k = 0
        nb_10k = 0
        nb_12k = 0
        total_resto = 0
        total_sortie=0
        total_service=0
        total_room =0
        if data.get('checkin_date'):
            domain.append(('date_order', '>=', data.get('checkin_date')))
        if data.get('checkout_date'):
            domain.append(('date_order', '<=', data.get('checkout_date')))
        docs = self.env['room.booking'].search(domain, order="date_order desc")
        sorties = self.env['purchase.order'].search(domain)
        total_sortie += sum(sorties.mapped('amount_total'))
        total_resto += sum(docs.mapped('amount_untaxed_food'))
        total_service += sum(docs.mapped('amount_untaxed_service'))
        total_room += sum(docs.mapped('amount_taxed_room'))

        nb_5k = len(self.env['room.booking'].search(domain))

        return {
            'doc_ids': docs.ids,
            'doc_model': 'room.booking',
            'docs': docs,
            'datas': data,
            'sorties':sorties,
            'total_sortie':total_sortie,
            'total_resto':total_resto,
            'total_room':total_room,
            'total_service':total_service

        }

