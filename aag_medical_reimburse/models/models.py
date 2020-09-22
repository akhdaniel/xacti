# -*- coding: utf-8 -*-

from odoo import models, fields, api


class aag_medical_reimburse(models.Model):
    _name = 'aag_medical_reimburse.aag_medical_reimburse'
    _description = 'aag_medical_reimburse.aag_medical_reimburse'

    idno = fields.Integer('IDNO')
    trndat = fields.Date('Trans. Date')
    cata = fields.Char('Category')
    medcod = fields.Char('Med-Code')
    patien = fields.Char('Patien')
    dr = fields.Char('Hospital/Docter')
    apotik = fields.Char('Apotik')
    medamt = fields.Integer('Med-Amount')
    remark = fields.Char('Remark')
    paydat = fields.Date('Payment Date')
    month = fields.Integer('Month')
    year = fields.Integer('Year')
    status = fields.Boolean('Status')
    flag1 = fields.Char('Flag-1')
    flag2 = fields.Char('Flag-2')
    flag3 = fields.Char('Flag-3')
    flag4 = fields.Char('Flag-4')
