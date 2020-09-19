# -*- coding: utf-8 -*-

from datetime import date, datetime, time, timedelta

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, tools, _, SUPERUSER_ID
import pdb
import dateutil.parser
from pytz import timezone

import logging
_logger = logging.getLogger(__name__)

class hr_payslip(models.Model):
    _name = 'hr.payslip'
    _inherit = 'hr.payslip'

    @api.model
    def get_inputs(self, contracts, date_from, date_to):
        res = super(hr_payslip, self).get_inputs(contracts, date_from, date_to)

        amount = 0
#=======================================
# HITUNG DEDUCTION 01-SALARY
#=======================================
        cr = self.env.cr 
        sql = "delete from hr_payslip_input where contract_id=%s and code=%s"
        cr.execute(sql, (self.contract_id.id, 'INPUT_DEDUC_01'))

        sql = """select sum(amount) from aag_other_deduction_aag_other_deduction where idno=%s and month=%s and year=%s and code=%s"""
        month = self.date_from.month 
        year = self.date_from.year
        cr.execute(sql, (self.employee_id.x_idno, month, year, '01'))
        result = cr.fetchone()
        if result:
            amount = result[0]

        res.append({
            'name': 'Other Deduction 01-Gaji Pokok',
            'code': 'INPUT_DEDUC_01',
            'amount': amount,
            'contract_id': self.contract_id.id 
        })
#=======================================
# HITUNG DEDUCTION 05-TRANSPORT
#=======================================
        cr = self.env.cr 
        sql = "delete from hr_payslip_input where contract_id=%s and code=%s"
        cr.execute(sql, (self.contract_id.id, 'INPUT_DEDUC_05'))

        sql = """select sum(amount) from aag_other_deduction_aag_other_deduction where idno=%s and month=%s and year=%s and code=%s"""
        month = self.date_from.month 
        year = self.date_from.year
        cr.execute(sql, (self.employee_id.x_idno, month, year, '05'))
        result = cr.fetchone()
        if result:
            amount = result[0]

        res.append({
            'name': 'Other Deduction 05-Transport',
            'code': 'INPUT_DEDUC_05',
            'amount': amount,
            'contract_id': self.contract_id.id 
        })
#=======================================
# HITUNG DEDUCTION 08-LAIN LAIN
#=======================================
        cr = self.env.cr 
        sql = "delete from hr_payslip_input where contract_id=%s and code=%s"
        cr.execute(sql, (self.contract_id.id, 'INPUT_DEDUC_08'))

        sql = """select sum(amount) from aag_other_deduction_aag_other_deduction where idno=%s and month=%s and year=%s and code=%s"""
        month = self.date_from.month 
        year = self.date_from.year
        cr.execute(sql, (self.employee_id.x_idno, month, year, '08'))
        result = cr.fetchone()
        if result:
            amount = result[0]

        res.append({
            'name': 'Other Deduction 08-Lain Lain',
            'code': 'INPUT_DEDUC_08',
            'amount': amount,
            'contract_id': self.contract_id.id 
        })

        return res         
