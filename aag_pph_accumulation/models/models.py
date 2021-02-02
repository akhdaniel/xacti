# -*- coding: utf-8 -*-

from odoo import models, fields, api


class aag_pph_accumulation(models.Model):
    _name = 'aag_pph_accumulation.aag_pph_accumulation'
    _description = 'aag_pph_accumulation.aag_pph_accumulation'

    idno = fields.Integer('IDNO')
    x_accyy= fields.Integer('Year')
    x_accmm= fields.Integer('Month')
    x_accgrs= fields.Integer('Gross')
    x_accovt= fields.Integer('Overtime')
    x_accmed= fields.Integer('Medical')
    x_accthr= fields.Integer('THR')
    x_accbon= fields.Integer('Bonus')
    x_accjht2= fields.Integer('JHT 2%')
    x_accpen1= fields.Integer('Pensiun 1%')
    x_pph_accgrs= fields.Integer('PPh Gross')
    x_pph_accovt= fields.Integer('PPh Overtime')
    x_pph_accmed= fields.Integer('PPh Medical')
    x_pph_accthr= fields.Integer('PPh THR')
    x_pph_accbon= fields.Integer('PPh Bonus')
    x_pph_nondtp= fields.Integer('Prev PPh Non-DTP')
    x_pph_dtp= fields.Integer('Prev PPh DTP')
    x_pph_total= fields.Integer('Prev PPh Total')
