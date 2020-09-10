# -*- coding: utf-8 -*-

from odoo import models, fields, api


class employee(models.Model):
    _name = 'hr.employee'
    _inherit = 'hr.employee'
    x_idno = fields.Integer(string='Employee IDNO')
    x_empsts = fields.Char(string='Employee Status')
    x_allcd = fields.Char(string='Grade Code')
    x_spmi = fields.Boolean(string='Union Membership')
    x_spmi_med = fields.Integer(string='Med. Donation Code')
    x_spmimed = fields.Integer(string='Med. Donation Code')
    x_nokop = fields.Char(string='Cooperation ID')
    x_nobpjskes = fields.Char(string='BPJS-Kes ID')
    x_bpjskesadd = fields.Integer(string='Add. BPJS-Kes')
    x_nobpjstk = fields.Char(string='BPJS-TK ID')
    x_nobpjspen = fields.Char(string='BPJS Pension ID')
    x_npwp = fields.Char(string='Tax ID / NPWP')

    idno = fields.Integer(string='IDNO')

    _sql_constraints = [
        ('x_idno_unique',
         'unique(x_idno)',
        'IDNO tidak boleh duplicate - must unique!'),
        ('x_nokop_unique',
         'unique(x_nokop)',
         'IDKOP tidak boleh duplicate - must unique!'),
        ('x_nobpjskes_unique',
         'unique(x_nobpjskes,x_idno)',
         'IDBPJSKES tidak boleh duplicate - must unique!'),
        ('x_bpjstk_unique',
         'unique(x_nobpjstk,x_idno)',
         'NOBPJSTK tidak boleh duplicate - must unique!'),
        ('x_nobpjspen_unique',
         'unique(x_nobpjspen,x_idno)',
         'IDNO tidak boleh duplicate - must unique!'),
        ('x_npwp_unique',
         'unique(x_npwp,x_idno)',
         'NPWP tidak boleh duplicate - must unique!'),
    ]

"""test by evans"""
"""test by haris"""

class contract(models.Model):
    _name = 'hr.contract'
    _inherit = 'hr.contract'
    x_tpk = fields.Integer(string='TPK')
    x_occup = fields.Integer(string='Grade Allowance')
    x_family = fields.Integer(string='Family Allowance')
    x_functional = fields.Integer(string='Functional Allowance')
    x_trans = fields.Integer(string='Transport Allowance')
    x_perform = fields.Integer(string='Performance Allowance')
    x_other = fields.Integer(string='Others Allowance')
    x_presence = fields.Integer(string='Presence Allowance')
    x_shift = fields.Integer(string='Daily SHift Allowance')
    x_ovtrate = fields.Integer(string='Hourly Overtime Rate')

class company(models.Model):
    _name = 'res.company'
    _inherit = 'res.company'
    x_meal = fields.Integer(string='Daily Meal Allowance')
    x_umsk = fields.Integer(string='UMSK')
    x_kwt_wage = fields.Integer(string='Contract Monthly Wage')
    x_kwt_trans = fields.Integer(string='Contract Daily Transpot')
    x_shift_op = fields.Integer(string='Daily Shift Allowance-Opr Level')
    x_shift_gl = fields.Integer(string='Daily Shift Allowance-GL Level')
    x_shift_sv = fields.Integer(string='Daily Shift Allowance-SV Level')
    x_shift_am = fields.Integer(string='Daily Shift Allowance-AM Level')
    x_shift_sm = fields.Integer(string='Daily Shift Allowance-SM Level')
    x_shift_dm = fields.Integer(string='Daily Shift Allowance-DM Level')