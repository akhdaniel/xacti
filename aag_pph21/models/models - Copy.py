# -*- coding: utf-8 -*-

from odoo import models, fields, api

class master_ptkp(models.Model):
    _name = 'aag_master_ptkp'

    name = fields.Char(string="PTKP Code")
    nominal = fields.Integer(string="PTKP Nominal")

class master_pkp(models.Model):
    _name = 'aag_master_pkp'

    rate = fields.Float(string="Tarif")
    minimum = fields.Integer(string="Penghasilan Minimum")
    maximum = fields.Integer(string="Penghasilan Maximum")
    company_id = fields.Many2one(string="Company", comodel_name="res.company")

class employee(models.Model):
    _name = 'hr.employee'

    _inherit = 'hr.employee'
    ptkp_id = fields.Many2one(string='PTKP Code',comodel_name='aag_master_ptkp')

class company(models.Model):
    _name = 'res.company'

    _inherit = 'res.company'
    pkp_ids = fields.One2many(string='Rate Penghasilan Kena Pajak', comodel_name='aag_master_pkp', inverse_name='company_id')

class aag_pph21_accumulation(models.Model):
    _name = 'aag_pph21_accumulation.aag_pph21_accumulation'
    _description = 'aag_pph21_accumulation.aag_pph21_accumulation'

    x_idno = fields.Integer('IDNO')
    x_mmfrom = fields.Integer('From Month')
    x_mmto = fields.Integer('To Month')
    x_yy = fields.Integer('Year')
    x_accovt = fields.Integer('Overtime.')
    x_accmed = fields.Integer('Medical.')
    x_accthr = fields.Integer('THR')
    x_accbon = fields.Integer('Bonus')
    x_accgrs = fields.Integer('Gross')
    x_accjth2 = fields.Integer('JHT 2%')
    x_accpen1 = fields.Integer('Pensiun 1%')
    x_pph_accovt = fields.Integer('PPh21 Overtime')
    x_pph_accmed = fields.Integer('PPh21 Medical')
    x_pph_accthr = fields.Integer('PPh21 THR')
    x_pph_accbon = fields.Integer('PPh21 Bonus')
    x_pph_accgrs = fields.Integer('PPh21 Gross') 