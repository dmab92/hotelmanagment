# -*- coding:Utf-8 -*-
from collections import Counter
from odoo import api, fields, models, _
from odoo.exceptions import UserError,ValidationError

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

        booking_details = self.env['room.booking.line'].search(domain, order='list_price asc')
        #booking_details = self.env['room.booking.line'].read_group(domain, fields=['list_price'], groupby=['list_price'],lazy=True, orderby=['list_price'])
        #print(type(booking_details))
        list_elt =lis_qty=[]
        qtys = []
        i=0
        # if 1:
        #     raise ValidationError(_(booking_details))
        #Get all the price
        for line in booking_details:
            list_elt.append(line['list_price'])
            lis_qty.append(line['uom_qty'])
        prices = list(set(list_elt))
        #get occurence of each price

        for price in prices:
            som = 0
            for line in booking_details:
                if price ==line['list_price'] :
                    som +=line['uom_qty']
            qtys.append(som)

        # if len(prices)== len(qtys):
        #     raise ValidationError(_("C'est parfait"))

            #qtys.append(Counter(list_elt)[i])

        sorties = self.env['purchase.order'].search(domain)
        total_sortie += sum(sorties.mapped('amount_total'))
        total_resto += sum(docs.mapped('amount_untaxed_food'))
        total_service += sum(docs.mapped('amount_untaxed_service'))
        total_room += sum(docs.mapped('amount_untaxed_room'))

        return {
            'doc_ids': docs.ids,
            'doc_model': 'room.booking',
            'docs': docs,
            'datas': data,
            'sorties':sorties,
            'total_sortie':total_sortie,
            'total_resto':total_resto,
            'total_room':total_room,
            'total_service':total_service,
            'booking_details':booking_details,
            'prices':prices,
            'qtys':qtys,

        }

