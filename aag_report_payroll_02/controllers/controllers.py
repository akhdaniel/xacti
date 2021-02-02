# -*- coding: utf-8 -*-
# from odoo import http


# class AagReportPayroll(http.Controller):
#     @http.route('/aag_report_payroll/aag_report_payroll/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/aag_report_payroll/aag_report_payroll/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('aag_report_payroll.listing', {
#             'root': '/aag_report_payroll/aag_report_payroll',
#             'objects': http.request.env['aag_report_payroll.aag_report_payroll'].search([]),
#         })

#     @http.route('/aag_report_payroll/aag_report_payroll/objects/<model("aag_report_payroll.aag_report_payroll"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('aag_report_payroll.object', {
#             'object': obj
#         })
