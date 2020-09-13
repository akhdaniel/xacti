# -*- coding: utf-8 -*-

from odoo import models, fields, api


class employee(models.Model):
    _name = 'hr.employee'
    _inherit = 'hr.employee'
    x_idno = fields.Integer(string='Employee IDNO')
    x_empsts = fields.Char(string='Employee Status')
    x_allcd = fields.Char(string='Grade Code')
    x_class = fields.Char(string='Class Code')
    x_direct = fields.Boolean(string='Direct Employee')
    x_spmi = fields.Boolean(string='Union Membership')
    x_spmi_med = fields.Integer(string='Med. Donation Code')
#   x_spmimed = fields.Integer(string='Med. Donation Code')
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
    x_stdtpk = fields.Integer(string='Standart TPK')
    x_stdtpk_m1 = fields.Integer(string='TPK Male-1')
    x_stdtpk_m2 = fields.Integer(string='TPK Male-2')
    x_stdtpk_f1 = fields.Integer(string='TPK Female-1')
    x_stdtpk_f2 = fields.Integer(string='TPK Female-2')
    x_stdtpk_f3 = fields.Integer(string='TPK Female-3')
    x_stdtpk_f4 = fields.Integer(string='TPK Female-4')
    x_meal = fields.Integer(string='Meal/Day')
    x_umsk = fields.Integer(string='UMSK/Month')
    x_kwt_wage = fields.Integer(string='KWT Monthly Wage')
    x_kwt_trans = fields.Integer(string='KWT Daily Transport')
    x_shift_op = fields.Integer(string='Shift Alw.-OP/Day')
    x_shift_gl = fields.Integer(string='Shift Alw.-GL/Day')
    x_shift_sv = fields.Integer(string='Shift Alw.-SV/Day')
    x_shift_am = fields.Integer(string='Shift Alw.-AM/Day')
    x_shift_sm = fields.Integer(string='Shift Alw.-SM/Day')
    x_shift_dm = fields.Integer(string='Shift Alw.-DM/Day')
    x_min_bpjskes = fields.Integer(string='Min. BPJS-Kes.')
    x_max_bpjskes = fields.Integer(string='Max. BPJS-Kes.')
    x_max_bpjspen = fields.Integer(string='Max. BPJS-Pensiun')