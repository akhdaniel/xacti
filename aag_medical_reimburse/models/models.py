# -*- coding: utf-8 -*-

from odoo import models, fields, api


class aag_medical_reimburse(models.Model):
    _name = 'aag_medical_reimburse.aag_medical_reimburse'
    _description = 'aag_medical_reimburse.aag_medical_reimburse'

    idno = fields.Integer('IDNO')
    
    amount = fields.Float('Amount')
    status = fields.Boolean('Status')
    month = fields.Integer('Month')
    year = fields.Integer('Year')