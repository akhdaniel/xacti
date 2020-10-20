# -*- coding: utf-8 -*-
# from odoo import http


# class AagPayslipPrint(http.Controller):
#     @http.route('/aag_payslip_print/aag_payslip_print/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/aag_payslip_print/aag_payslip_print/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('aag_payslip_print.listing', {
#             'root': '/aag_payslip_print/aag_payslip_print',
#             'objects': http.request.env['aag_payslip_print.aag_payslip_print'].search([]),
#         })

#     @http.route('/aag_payslip_print/aag_payslip_print/objects/<model("aag_payslip_print.aag_payslip_print"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('aag_payslip_print.object', {
#             'object': obj
#         })
