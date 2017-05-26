# -*- coding: utf-8 -*-

from openerp import models, fields, api
from odoo.addons.website.models.website import slug
from inherited_website import defaultRouteIntro

class Blog(models.Model):
    """Inherit model Blog blog:
     - Add new field singleBlogPost, blog_post_ids
     - Update all blog post belong blog blog will unpublished except latest one, when singleBlogPost checked
    """
    _name = 'blog.blog'
    _inherit = ['blog.blog','ari.base.model','ari.jumbo.model']
    
    @api.depends('code')
    def _getDisplayName(self):
        for record in self:
            record.display_name = record.code
            
    display_name = fields.Char(string="DisplayName", store=True, compute='_getDisplayName')
    singleBlogPost = fields.Boolean(string='Single Blog', default = False, help="True: all blog post belong this blog automatic unpublished except latest one")
    blog_post_ids = fields.One2many('blog.post', 'blog_id', readonly = True)
    code = fields.Char(required=True)
    #This field using one2many, but only one blog link with only one to menu
    website_menu_ids = fields.One2many('website.menu', 'blog_id', string="Menu linked to this blog", readonly = 1)
    
    _sql_constraints = [('blog_code_unique_check', 
                        'unique(code)',
                        "The code of the Blog must be unique"
                        ),
                        ('blog_name_unique_check', 
                        'unique(name)',
                        "The name of the Blog must be unique")]
    
    @api.constrains('singleBlogPost')
    def _check_singleblog(self):
        """This constrains update all blog post belong blog blog will unpublished except latest one, when singleBlogPost checked"""
        for blog in self:
            if blog.singleBlogPost and blog.blog_post_ids:
                sqlCommand = """UPDATE blog_post 
                                SET website_published=case 
                                WHEN write_date = (SELECT 
                                                        max(write_date) 
                                                    FROM blog_post 
                                                    WHERE website_published and blog_id=%s) 
                                THEN True 
                                ELSE False end 
                                WHERE blog_id=%s and website_published""" % (self.id, self.id)
                self.env.cr.execute(sqlCommand)
                # latestBlog = None
                # for blog_post in filter(lambda bp: bp.website_published, blog.blog_post_ids):
                #     writedDate = blog_post.write_date
                #     blog_post.website_published = False
                #     blog_post.write_date = writedDate
                #     if not latestBlog or latestBlog.write_date < blog_post.write_date:
                #         latestBlog = blog_post
                # if latestBlog:
                #     latestBlog.website_published = True
                
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if operator not in ('ilike', 'like', '=', '=like', '=ilike'):
            return super(Blog, self).name_search(name, args, operator, limit)
        args = args or []
        domain = ['|', ('code', operator, name), ('name', operator, name)]
        recs = self.search(domain + args, limit=limit)
        return recs.name_get()

class BlogPost(models.Model):
    """Inherit model Blog Post:
     - Update all blog post belong blog blog will unpublished except current record is published one, when singleBlogPost checked
    """
    _inherit = ["blog.post","ari.base.model"]
    _name = 'blog.post'
    
    summary = fields.Text('Summary', translate=True)
    
    @api.constrains('website_published','blog_id')
    def _check_website_published_blog(self):
        """This constrains update all blog post belong blog blog will unpublished except current published one, when singleBlogPost checked"""
        if self.website_published and self.blog_id.singleBlogPost:
            sqlCommand = """UPDATE blog_post 
                            SET website_published=False 
                            WHERE blog_id=%s and website_published and id!=%s """ % (self.blog_id.id, self.id)
            self.env.cr.execute(sqlCommand)
            
    @api.multi
    def _compute_website_url(self):
        super(BlogPost, self)._compute_website_url()
        for blog_post in self:
            blog_post.website_url = "%s/%s/post/%s" % (defaultRouteIntro, slug(blog_post.blog_id), slug(blog_post))