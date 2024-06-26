# -*- coding: utf-8 -*-
################################################################################
#
################################################################################
{
    'name': 'Hotel Repos Roi',
    'version': '16.0.1.0.0',
    'category': 'Industries',
    'summary': """A complete Hotel Management System that cover all areas of 
     Hotel services""" ,
    'description': """The module helps you to manage rooms, amenities, 
     services, food, events and vehicles. End Users can book rooms and reserve 
     foods from hotel.""",
    'author': 'Boris MENI',
    'company': 'MT CONSULTING SARL',
    'maintainer': 'MT CONSULTING SARL',
    'website': 'https://www.mtconsulting.cm',
    'depends': ['base','account', 'event', 'fleet', 'lunch'],
    #'depends': ['base'],
    'data': [
        'security/hotel_management_odoo_groups.xml',
        'security/hotel_management_odoo_security.xml',
        'security/ir.model.access.csv',
        'data/ir_data_sequence.xml',
        'views/account_move_views.xml',
        'views/hotel_menu_views.xml',
        'views/hotel_amenity_views.xml',
        'views/hotel_service_views.xml',
        'views/hotel_floor_views.xml',
        'views/hotel_room_views.xml',
        'views/lunch_product_views.xml',
        'views/fleet_vehicle_model_views.xml',
        'views/room_booking_views.xml',
        'views/maintenance_team_views.xml',
        'views/maintenance_request_views.xml',
        'views/cleaning_team_views.xml',
        'views/cleaning_request_views.xml',
        'views/food_booking_line_views.xml',
        'views/dashboard_view.xml',
        'wizard/room_booking_detail_views.xml',
        'wizard/sale_order_detail_views.xml',
        'views/reporting_views.xml',
        'report/room_booking_reports.xml',
        'report/sale_order_reports.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'hotel_management_odoo/static/src/js/action_manager.js',
            'hotel_management_odoo/static/src/css/dashboard.css',
            'hotel_management_odoo/static/src/js/dashboard_action.js',
            'hotel_management_odoo/static/src/xml/dashboard_templates.xml',
        ],
    },
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}

