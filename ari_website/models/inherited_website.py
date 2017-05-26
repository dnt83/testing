from openerp import models, fields, api
from urlparse import urljoin
from odoo.addons.website.models.website import slug

defaultRouteIntro = '/introduce/ari-logistics/'

class Website(models.Model):
    _inherit = "website"
    
    post_per_page = fields.Integer('Post per page', default=8)
    # default_route_intro = fields.Char("Default Route Intro", default=)
    
class WebsiteMenu(models.Model):
    """
        Add field active to website menu, to hide unused menu (menu created by default menu)
    """
    _name = "website.menu"
    _inherit = "website.menu"
    
    #Find a menu with URL, find util find submenu or end of path
    def findMenu(self, urlPath):
        res = False
        while not res and len(urlPath.split('/'))>0:
            res = self.search([('url', '=', urlPath)], limit=1)
            splitURL = urlPath.split('/')
            urlPath = '/'.join(splitURL[:len(splitURL)-1])
        return res
    
    @api.model
    # Set default value Active = True when user create new menu (default active is fasle when system create)
    def _default_active(self):
        return self.env.context.get('set_default_active', False)
    
    active = fields.Boolean(default=_default_active)
    manualUrl = fields.Char("URL", default='')
    url = fields.Char(string="New URL", store=True, compute='_getNewUrl')
    blog_id = fields.Many2one('blog.blog', string='Blog')
    full_name = fields.Char(string='Full Name', compute="_getFullName", readonly = 1)

    _sql_constraints = [('blog_menu_unique_check', 
                        'unique(blog_id)',
                        "Allow Only One menu link to a blog"
                        )]
                        
    @api.depends('name', 'parent_id', 'parent_id.name')
    def _getFullName(self):
        for record in self:
            record.full_name = "%s / %s"  % (record.parent_id.name, record.name) if record.parent_id else record.name
    
    @api.depends('manualUrl', 'blog_id', 'blog_id.code')
    def _getNewUrl(self):
        for record in self:
            record.url = urljoin(defaultRouteIntro, slug(record.blog_id)) if record.blog_id else record.manualUrl
            
    @api.multi
    def name_get(self):
        result = []
        for menu in self:
            result.append((menu.id, menu.full_name))
        return result
    