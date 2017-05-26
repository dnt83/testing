# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class WebsiteConfigSettings(models.TransientModel):

    _inherit = 'website.config.settings'
    
    post_per_page = fields.Integer(related='website_id.post_per_page')
    # default_route_intro = fields.Char(related='website_id.default_route_intro')