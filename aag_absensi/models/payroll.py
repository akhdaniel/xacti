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
# HITUNG CUTI LIBUR
#=======================================
        cr = self.env.cr 
        sql = "delete from hr_payslip_input where contract_id=%s and code=%s"
        cr.execute(sql, (self.contract_id.id, 'INPUT_ABS_01'))

        sql = """select count(*) from aag_absensi_aag_absensi where idno=%s and month=%s and year=%s and code=%s"""
        month = self.date_from.month 
        year = self.date_from.year
        cr.execute(sql, (self.employee_id.x_idno, month, year, 1))
        result = cr.fetchone()
        if result:
            amount = result[0]

        res.append({
            'name': 'Absensi 01',
            'code': 'INPUT_ABS_01',
            'amount': amount,
            'contract_id': self.contract_id.id 
        })
#=======================================
# HITUNG SAKIT (SD) 
#=======================================        
        cr = self.env.cr 
        sql = "delete from hr_payslip_input where contract_id=%s and code=%s"
        cr.execute(sql, (self.contract_id.id, 'INPUT_ABS_05'))

        sql = """select count(*) from aag_absensi_aag_absensi where idno=%s and month=%s and year=%s and code=%s"""
        month = self.date_from.month 
        year = self.date_from.year
        cr.execute(sql, (self.employee_id.x_idno, month, year, 5))
        result = cr.fetchone()
        if result:
            amount = result[0]

        res.append({
            'name': 'Absensi 05',
            'code': 'INPUT_ABS_05',
            'amount': amount,
            'contract_id': self.contract_id.id 
        })
#=======================================
# HITUNG ABSENT (05)
#=======================================
        cr = self.env.cr 
        sql = "delete from hr_payslip_input where contract_id=%s and code=%s"
        cr.execute(sql, (self.contract_id.id, 'INPUT_ABS_06'))

        sql = """select count(*) from aag_absensi_aag_absensi where idno=%s and month=%s and year=%s and code=%s"""
        month = self.date_from.month 
        year = self.date_from.year
        cr.execute(sql, (self.employee_id.x_idno, month, year, 6))
        result = cr.fetchone()
        if result:
            amount = result[0]

        res.append({
            'name': 'Absensi 06',
            'code': 'INPUT_ABS_06',
            'amount': amount,
            'contract_id': self.contract_id.id 
        })
#=============================

        return res         
