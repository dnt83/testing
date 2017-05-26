# -*- coding: utf-8 -*-

from openerp import models, fields, api


class ProductPublicCategory(models.Model):
     _inherit = ['ari.base.model', 'product.public.category']
     _name = "product.public.category"