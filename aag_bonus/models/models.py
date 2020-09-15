# -*- coding: utf-8 -*-

from odoo import models, fields, api


class aag_bonus(models.Model):
    _name = 'aag_bonus.aag_bonus'
    _description = 'aag_bonus.aag_bonus'

    idno = fields.Integer('IDNO')
    
    amount = fields.Integer('Amount')
    std_bonus = fields.Integer('Bonus 100%')
    percentage = fields.Float('Percentage')
    remark = fields.Char('Remark')
    month = fields.Integer('Month')
    year = fields.Integer('Year')
    status = fields.Boolean('Status')