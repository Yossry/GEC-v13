# -*- coding: utf-8 -*-
# from odoo import http


# class CustomLibro(http.Controller):
#     @http.route('/custom_libro/custom_libro/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_libro/custom_libro/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_libro.listing', {
#             'root': '/custom_libro/custom_libro',
#             'objects': http.request.env['custom_libro.custom_libro'].search([]),
#         })

#     @http.route('/custom_libro/custom_libro/objects/<model("custom_libro.custom_libro"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_libro.object', {
#             'object': obj
#         })
