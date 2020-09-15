# -*- coding: utf-8 -*-
# from odoo import http


# class AagImportAttendance(http.Controller):
#     @http.route('/aag_import_attendance/aag_import_attendance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/aag_import_attendance/aag_import_attendance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('aag_import_attendance.listing', {
#             'root': '/aag_import_attendance/aag_import_attendance',
#             'objects': http.request.env['aag_import_attendance.aag_import_attendance'].search([]),
#         })

#     @http.route('/aag_import_attendance/aag_import_attendance/objects/<model("aag_import_attendance.aag_import_attendance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('aag_import_attendance.object', {
#             'object': obj
#         })
