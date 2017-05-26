import werkzeug
import werkzeug.urls

import mimetypes
import odoo

from odoo import http, fields, SUPERUSER_ID, _

from odoo.http import request

from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from odoo import tools

#from odoo.addons.website_crm.controllers.main import contactus

from ..models.inherited_website import defaultRouteIntro

# class ARIWebsiteUnderConstruction(openerp.addons.website.controllers.main.Website): 
#   @http.route('/', auth='public', website=True)
#   def index(self, **kw):
#     return "<strong>Our website is under construction! Please check back regurlarly!</strong>"

class ARIWebsite(http.Controller):
  def website_posts(self, blog_name="", blogCategory = False, tag_name_list=[], post_ids=[], page_url='/', page=1,
                   template=['ari_website.show_post', 'ari_website.show_page_list_posts'], other_domain_search=[], **kwargs):
      """
      Getting all posts of blog(s) to prepare to show
          - If only 1 post return, show the post
          - If more than 1 post return, list these posts
          - Using other_domain_search for special search for example tag_ids.name
      """
      def _tag_search(search_domain):
        """
        blog.tag la truong many2many nen khi search voi dieu kien NOT
        ket qua tra ve se khong dung nhu mong muon. Method nay xu ly dieu kien
        search cua tag
        :return: search_domain
        """
        not_in_tags_search = filter(lambda s: s[0] == 'tag_ids.name' and s[1] == 'not in', search_domain)
        #not_in_tags_search.insert(0, '!')
        if not_in_tags_search:
          search_domain.remove(not_in_tags_search[0])
          post_ids_tags_search = http.request.env['blog.post'].search(['!', not_in_tags_search[0]]).mapped('id')
          search_domain.append(('id', 'not in', post_ids_tags_search))
        return search_domain
  
      def sd(date):
        """
         Dinh dang ngay thang theo odoo server settings
        :return: dd-mm-yyyy
        """
        return date.strftime(tools.DEFAULT_SERVER_DATETIME_FORMAT)
  
      today = datetime.today()
  
      announcements = http.request.env['blog.post'].search(
        [('blog_id', '=', 'Announcement'), ("create_date", ">=", sd(today - relativedelta(days=7)))])
      funfacts = http.request.env['blog.post'].search([('blog_id', '=', 'Fun Fact')])
      #events = http.request.env['event.event'].search([("date_begin", ">=", sd(today))], limit=6)
      events = []
      search_domain=[]
      if post_ids:
        result = post_ids
      elif blogCategory:
        result = blogCategory.blog_post_ids
      else:
        if blog_name:
          search_domain = [('blog_id', '=', blog_name)]
          if tag_name_list:
            search_domain.append(('tag_ids.name', 'in', tag_name_list))
      
        #handle for not in tags search
        
        other_domain_search = _tag_search(other_domain_search)
        search_domain += other_domain_search
        if search_domain:
          result = http.request.env['blog.post'].search(search_domain, **kwargs)
        else:
          result = []
      if len(result) <= 1:
        # Return only one post
        try:
            request.website.get_template(template[0]).name
        except Exception, e:
            return request.env['ir.http']._handle_exception(e, 404)
        #Get Submenu
        if not blogCategory:
          blogCategory = result.blog_id
        subMenus = blogCategory.website_menu_ids[0].parent_id.child_id if blogCategory.website_menu_ids and blogCategory.website_menu_ids[0].parent_id else []
        
        return http.request.render(template[0],
                                   {'blogData': result, 'announcements': announcements, 'ffacts': funfacts, 'events': events,
                                    'jumboData': blogCategory, 'subMenus': subMenus
                                   })
      elif len(result) > 1:
        # Return posts -> list posts
        # Handler pager
        try:
            request.website.get_template(template[1]).name
        except Exception, e:
            return request.env['ir.http']._handle_exception(e, 404)
        postPerPage = http.request.website.post_per_page
        pager = request.website.pager(
          url=page_url,
          page=page,
          total=len(result),
          step=postPerPage
        )
        # limit and offset result
        
        search_domain = [('id','in',result.mapped('id'))]
        result = http.request.env['blog.post'].search(search_domain, offset=(page - 1) * postPerPage,
                                                      limit=postPerPage)
        
        #Get Submenu
        if not blogCategory:
          blogCategory = result.blog_id
        subMenus = blogCategory.website_menu_ids[0].parent_id.child_id if blogCategory.website_menu_ids and blogCategory.website_menu_ids[0].parent_id else []
        jumboData = blogCategory
        
        return http.request.render(template[1], {
          'blogDatas': result,
          'pager': pager,
          'announcements': announcements,
          'ffacts': funfacts,
          'jumboData': jumboData,
          'subMenus': subMenus
        })
        
  
  #Route Blog Category & Blog
  @http.route(['%s<model("blog.blog"):category>' % defaultRouteIntro,
              '%s<model("blog.blog"):category>/post/<model("blog.post",[("blog_id",=,category[0])]"):posts>' % defaultRouteIntro,
              '%s<model("blog.blog"):category>/<model("blog.post",[("blog_id",=,category[0])]"):posts>' % defaultRouteIntro], type='http',  auth='public', website=True)
  def intro(self, category, enable_editor=None, edit_translations = None, posts = False):
    return self.website_posts(blogCategory = category, post_ids=posts, template=['ari_website.show_post', 'ari_website.show_page_list_posts'])
    
  @http.route('/ari/update', type='http', auth="public", website=True, methods=['POST'])
  def ari_post_update(self, updateObject, updateInfo, recordID, returnURL, **post):
      """ Duplicate a blog.

      :param blog_post_id: id of the blog post currently browsed.

      :return redirect to the new blog created
      """
      if updateInfo and recordID and updateObject and type(eval(updateInfo))==type({}):
        if not request.session.uid:
            return {'error': 'anonymous_user'}
        Model = request.env[updateObject]
        record = Model.browse(int(recordID))
        record.sudo().write(eval(updateInfo))
      return request.redirect(returnURL)
      