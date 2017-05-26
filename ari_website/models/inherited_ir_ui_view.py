# -*- coding: ascii -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)

class View(models.Model):
    _name = "ir.ui.view"
    _inherit = "ir.ui.view"

    @api.multi
    def render(self, values=None, engine='ir.qweb'):
        """
        Modify render method to add ARI information to the homepage
        """
        values = values or {}
        if engine=='ir.qweb' and values.get('path','') == 'homepage':
            #Get data show in Jumbo Homepage
            show_obj = 'product.public.category'
            show_pool = self.env[show_obj]
            domainSearch = [('parent_id',">=",1)] #Not show Root Category
            result = show_pool.search(domainSearch)
            values['jumboDatas'] = result
            values['jumboData'] = result[0] if result else False
        
        res=super(View, self).render(values, engine=engine)
        return res