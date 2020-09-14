# -*- coding: utf-8 -*-

from odoo import models, fields, api


class aag_koperasi(models.Model):
    _name = 'aag_koperasi.aag_koperasi'
    _description = 'aag_koperasi.aag_koperasi'

    # name = fields.Char('NIK')
    x_idno = fields.Integer('IDNO')
    x_amount = fields.Float('Potongan')
    x_month = fields.Integer('Month')
    x_year = fields.Integer('Year')
    x_status = fields.Boolean('Status')
    x_remark = fields.Char('Remark')