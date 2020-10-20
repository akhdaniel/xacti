# -*- coding: utf-8 -*-

from odoo import models, fields, api


class aag_absensi(models.Model):
    _name = 'aag_absensi.aag_absensi'
    _description = 'aag_absensi.aag_absensi'

    idno = fields.Integer('IDNO')
    date = fields.Date('Date')
    month = fields.Integer('Month')
    year = fields.Integer('Year')    
    code = fields.Integer('Code')
    remark = fields.Char('Remark')
    status = fields.Boolean('Status')

