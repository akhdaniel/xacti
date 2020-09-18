# -*- coding: utf-8 -*-

from odoo import models, fields, api


class aag_shift(models.Model):
    _name = 'aag_shift.aag_shift'
    _description = 'aag_shift.aag_shift'

    idno = fields.Integer('IDNO')
    
    amount = fields.Integer('Amount')
    code = fields.Char('Code')
    remark = fields.Char('Remark')
    month = fields.Integer('Month')
    year = fields.Integer('Year')
    status = fields.Boolean('Status')