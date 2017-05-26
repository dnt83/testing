# -*- coding: utf-8 -*-
{
    'name': "ari_website",

    'summary': """
        Customize and deploy Website for Ari Logistics""",

    'description': """
    """,

    'author': "TD-Team",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Ari Website',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['im_livechat', 'website_blog', 'website_sale', 'document'],

    # always loaded
    'data': [
        'data/data_blog.xml',
        'data/data_menu.xml',
        'data/data_website.yml',
        'data/data_product.xml',
        # 'security/ir.model.access.csv',
        'security/security.xml',
        'views/website_config_views.xml',
        'views/templates.xml',
        'views/ari_website_views.xml',
        'views/product.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}