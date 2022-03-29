# -*- coding: utf-8 -*-
# from odoo import http


# class Salsabakery(http.Controller):
#     @http.route('/salsabakery/salsabakery/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/salsabakery/salsabakery/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('salsabakery.listing', {
#             'root': '/salsabakery/salsabakery',
#             'objects': http.request.env['salsabakery.salsabakery'].search([]),
#         })

#     @http.route('/salsabakery/salsabakery/objects/<model("salsabakery.salsabakery"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('salsabakery.object', {
#             'object': obj
#         })
