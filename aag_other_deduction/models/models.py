# -*- coding: utf-8 -*-

from odoo import models, fields, api


class aag_other_deduction(models.Model):
    _name = 'aag_other_deduction.aag_other_deduction'
    _description = 'aag_other_deduction.aag_other_deduction'

    idno = fields.Integer('IDNO')
    
    amount = fields.Integer('Amount')
    code = fields.Char('Code')
    remark = fields.Char('Remark')
    month = fields.Integer('Month')
    year = fields.Integer('Year')
    status = fields.Boolean('Status')