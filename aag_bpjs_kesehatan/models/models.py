# -*- coding: utf-8 -*-

from odoo import models, fields, api


class aag_bpjs_kesehatan(models.Model):
    _name = 'aag_bpjs_kesehatan.aag_bpjs_kesehatan'
    _description = 'aag_bpjs_kesehatan.aag_bpjs_kesehatan'

    idno = fields.Integer('IDNO')
    
    amount_dtk = fields.Integer('BPJS-Kes DTK')
    amount_dtp = fields.Integer('BPJS-Kes DTP')
    code = fields.Char('Code')
    remark = fields.Char('Remark')
    month = fields.Integer('Month')
    year = fields.Integer('Year')
    status = fields.Boolean('Status')