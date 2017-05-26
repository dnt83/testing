# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import html_translate, _


class ARIJumboModel(models.AbstractModel):
    _name = "ari.jumbo.model"
    
    jumbo_conent = fields.Html('Jumbo Content', translate=html_translate, sanitize_attributes=False)
    jumbo_select = fields.Selection([('default', 'Default Jumbo'), ('custom', 'Custom Jumbo'),('none','No Jumbo')], required=True, default='default')
    
class ARIBaseModel(models.AbstractModel):
    ''' ARIBase model is meant to be inherited by any model that needs to
        image link to attachments
    '''
    _name = "ari.base.model"
    
    @api.depends()
    def _get_img_url_ids(self):
        
        for record in self:
            result = []
            attachments = self.env['ir.attachment'].search([('res_model','=',self._name), ('res_id','=',record.id)])
            imgULRIDS = [res.id for res in attachments  if res.mimetype and res.mimetype.find("image/")>=0]
            result = attachments.mapped('id')
            
            record.img_url_ids = imgULRIDS
            
            record.attachment_ids = result
            if imgULRIDS:
                import random
                record.img_url_ramdon_id = random.choice(imgULRIDS)
            else:
                record.img_url_ramdon_id = False


    img_url_ids = fields.One2many('ir.attachment', string="Image URLs", compute='_get_img_url_ids', multi='_get_attachment_url')
    attachment_ids = fields.One2many('ir.attachment', string="Image URLs", compute='_get_img_url_ids', multi='_get_attachment_url')
    img_url_ramdon_id = fields.Many2one('ir.attachment', string="Image URL Ramdom", compute='_get_img_url_ids',  multi='_get_attachment_url')