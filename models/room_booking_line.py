# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Unnimaya C O (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
from datetime import datetime

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError

class RoomBookingtype(models.Model):
    """Model that handles the room booking form"""
    _name = "room.booking.type"
    _description = "Hotel Folio Type"
    _rec_name = 'name'

    name = fields.Char("Type de Sejour")

class RoomBookingLine(models.Model):
    """Model that handles the room booking form"""
    _name = "room.booking.line"
    _description = "Hotel Folio Line"
    _rec_name = 'room_id'
    _order = 'id desc'

    @tools.ormcache()
    def _set_default_uom_id(self):
        return self.env.ref('uom.product_uom_day')

    booking_id = fields.Many2one("room.booking", string="Booking",
                                 help="Indicates the Room",
                                 ondelete="cascade")
    checkin_date = fields.Datetime(string="Check In",
                                   help="You can choose the date,"
                                        " Otherwise sets to current Date",

                                   required=True)
    checkout_date = fields.Datetime(string="Check Out",
                                    help="You can choose the date,"
                                         " Otherwise sets to current Date",

                                    required=True)
    room_id = fields.Many2one('hotel.room', string="Room",
                              domain=[('status', '=', 'available')],
                              help="Indicates the Room",
                              required=True)
    uom_qty = fields.Float(string="Duration",
                           help="The quantity converted into the UoM used by "
                                "the product" )



    uom_id = fields.Many2one('uom.uom',
                             default=_set_default_uom_id,
                             string="Unit of Measure",
                             help="This will set the unit of measure used",
                             readonly=True)
    list_price = fields.Float(string='Rent',
                              digits='Product Price',
                              help="The rent price of the selected room.")
    tax_ids = fields.Many2many('account.tax',
                               'hotel_room_order_line_taxes_rel',
                               'room_id', 'tax_id',
                               related='room_id.taxes_ids',
                               string='Taxes',
                               help="Default taxes used when selling the room.",
                               domain=[('type_tax_use', '=', 'sale')])
    currency_id = fields.Many2one(string='Currency',
                                  related='booking_id.pricelist_id.currency_id',
                                  help='The currency used')
    price_subtotal = fields.Float(
        string="Subtotal",
        compute='_compute_price_subtotal', help="Total Price excluding Tax",
        store=True)
    price_tax = fields.Float(
        string="Total Tax",
        compute='_compute_price_subtotal', help="Tax Amount",
        store=True)
    price_total = fields.Float(
        string="Total",
        compute='_compute_price_subtotal', help="Total Price including Tax",
        store=True)
    state = fields.Selection(
        related='booking_id.state',
        string="Order Status", help=" Status of the Order",
        copy=False)
    #precompute = True
    booking_line_visible = fields.Boolean(default=False,
                                          string="Booking Line Visible",
                                          help="If True, then Booking Line will"
                                               " be visible")

    state_pay = fields.Selection([('draft', 'Non Payé'),
                                 ('pay', 'Payé'),
                                 ], default='draft', string="Etat paiement")
    state_mod = fields.Selection([('cash', 'CASH'),
                                  ('momo', 'MOMO'),
                                  ('om', 'OM'),
                                  ('virement', 'VIREMENT'),

                                  ] ,default='cash', string="Mode paiement")
    #user = fields.Many2one("res.users", "Receptionist",default=lambda self: self.env.user )

    # hour_qty = fields.Float(string="Number of hours",
    #                         help="Difrrence beetewen hours", readonly=True, )
    number_person = fields.Integer(string="Nombre de personne")

    user = fields.Many2one("res.users", "Receptionist", default=lambda self: self.env.user)
    #user = fields.Many2one("room.booking.type", "Receptionist", default=lambda self: self.env.user)

    nuite_siete = fields.Selection([
        ('SIESTE', 'Sieste'),
        ('NUITEE', 'Nuité') ], default='NUITEE', string="Type")

    @api.onchange("checkin_date", "checkout_date")
    def _onchange_checkin_date(self):
        """
        When you change checkin_date or checkout_date it will check
        and update the qty of hotel service line
        -----------------------------------------------------------------
        @param self: object pointer
        """
        if self.checkout_date < self.checkin_date:
            raise ValidationError(
                _("Checkout must be greater or equal checkin date"))
        if self.checkin_date and self.checkout_date:
            diffdate = self.checkout_date - self.checkin_date
            qty = diffdate.days
            if diffdate.total_seconds() > 0:
                qty = qty + 1
            self.uom_qty = qty

    @api.onchange("nuite_siete","room_id")
    def _onchange_checkin_date(self):
        """
        When you change type af reservation(night or sieste)
        and update the price of hotel service line
        -----------------------------------------------------------------
        @param self: object pointer
        """
        if self.nuite_siete =='NUITEE':
            self.list_price=  self.room_id.list_price
        if self.nuite_siete =='SIESTE':
            self.list_price=  self.room_id.price_siete


    #list_price
    @api.depends('uom_qty', 'list_price','tax_ids')
    def _compute_price_subtotal(self):
        """
        Compute the amounts of the room booking line.
        """

        for line in self:
            tax_results = self.env['account.tax']._compute_taxes(
                [line._convert_to_tax_base_line_dict()])
            totals = list(tax_results['totals'].values())[0]
            amount_untaxed = totals['amount_untaxed']
            amount_tax = totals['amount_tax']
            line.update({
                'price_subtotal': amount_untaxed,
                'price_tax': amount_tax,
                'price_total': amount_untaxed + amount_tax,
            })
            if self.env.context.get('import_file',
                                    False) and not self.env.user. \
                    user_has_groups('account.group_account_manager'):
                line.tax_id.invalidate_recordset(
                    ['invoice_repartition_line_ids'])

    def _convert_to_tax_base_line_dict(self):
        """ Convert the current record to a dictionary in order to use the
        generic taxes computation method
        defined on account.tax.

        :return: A python dictionary.
        """
        self.ensure_one()
        return self.env['account.tax']._convert_to_tax_base_line_dict(
            self,
            partner=self.booking_id.partner_id,
            currency=self.currency_id,
            taxes=self.tax_ids,
            price_unit=self.list_price,
            quantity=self.uom_qty,
            price_subtotal=self.price_subtotal,
        )
