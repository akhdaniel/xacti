# -*- coding: utf-8 -*-

from odoo import models, fields, api


class aag_thr(models.Model):
    _name = 'aag_thr.aag_thr'
    _description = 'aag_thr.aag_thr'

    idno = fields.Integer('IDNO')
    
    amount = fields.Integer('Amount')
    std_thr = fields.Integer('THR 100%')
    percentage = fields.Float('Percentage')
    remark = fields.Char('Remark')
    month = fields.Integer('Month')
    year = fields.Integer('Year')
    status = fields.Boolean('Status')