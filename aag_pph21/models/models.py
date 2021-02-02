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

# class aag_salary_ytd(models.Model):
#     _name = 'aag_salary_ytd'
#     _description = 'aag_salary_ytd'

#     m_idno = fields.Integer('IDNO')
#     m_basic = fields.Integer("Basic Salary Add", )
#     m_tpk = fields.Integer("TPK", )
#     m_occup = fields.Integer("Grade Allw", )
#     m_functional = fields.Integer("Functional Allw", )
