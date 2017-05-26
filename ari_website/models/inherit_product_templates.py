from openerp import models, fields, api


class ProductTemplate(models.Model):
    _name = 'product.template'
    
    # product_ids = fields.One2many('product.product','')