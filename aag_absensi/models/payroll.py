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
# HITUNG CUTI LIBUR (FULL DAY)
#=======================================
        cr = self.env.cr 
        sql = "delete from hr_payslip_input where contract_id=%s and code=%s"
        cr.execute(sql, (contracts.id, 'INPUT_ABS_01'))

        sql = """select count(*) from aag_absensi_aag_absensi where idno=%s and month=%s and year=%s and code=%s"""
        month = date_from.month 
        year = date_from.year
        cr.execute(sql, (contracts.employee_id.x_idno, month, year, 1))
        result = cr.fetchone()
        if result:
            amount = result[0]

        res.append({
            'name': 'Absensi 01-Cuti Libur',
            'code': 'INPUT_ABS_01',
            'amount': amount,
            'contract_id': contracts.id 
        })
#=======================================
# HITUNG CUTI LIBUR (HALF DAY)
#=======================================
        cr = self.env.cr 
        sql = "delete from hr_payslip_input where contract_id=%s and code=%s"
        cr.execute(sql, (contracts.id, 'INPUT_ABS_11'))

        sql = """select count(*) from aag_absensi_aag_absensi where idno=%s and month=%s and year=%s and code=%s"""
        month = date_from.month 
        year = date_from.year
        cr.execute(sql, (contracts.employee_id.x_idno, month, year, 11))
        result = cr.fetchone()
        if result:
            amount = result[0]

        res.append({
            'name': 'Absensi 11-Cuti Setengah Hari',
            'code': 'INPUT_ABS_11',
            'amount': amount,
            'contract_id': contracts.id 
        })
#=======================================
# HITUNG SAKIT (05) 
#=======================================        
        cr = self.env.cr 
        sql = "delete from hr_payslip_input where contract_id=%s and code=%s"
        cr.execute(sql, (contracts.id, 'INPUT_ABS_05'))

        sql = """select count(*) from aag_absensi_aag_absensi where idno=%s and month=%s and year=%s and code=%s"""
        month = date_from.month 
        year = date_from.year
        cr.execute(sql, (contracts.employee_id.x_idno, month, year, 5))
        result = cr.fetchone()
        if result:
            amount = result[0]

        res.append({
            'name': 'Absensi 05-Sakit',
            'code': 'INPUT_ABS_05',
            'amount': amount,
            'contract_id': contracts.id 
        })
#=======================================
# HITUNG ABSENT (06)
#=======================================
        cr = self.env.cr 
        sql = "delete from hr_payslip_input where contract_id=%s and code=%s"
        cr.execute(sql, (contracts.id, 'INPUT_ABS_06'))

        sql = """select count(*) from aag_absensi_aag_absensi where idno=%s and month=%s and year=%s and code=%s"""
        month = date_from.month 
        year = date_from.year
        cr.execute(sql, (contracts.employee_id.x_idno, month, year, 6))
        result = cr.fetchone()
        if result:
            amount = result[0]

        res.append({
            'name': 'Absensi 06-Absent',
            'code': 'INPUT_ABS_06',
            'amount': amount,
            'contract_id': contracts.id 
        })

#=======================================
# HITUNG CUTI HAMIL (07)
#=======================================
        cr = self.env.cr 
        sql = "delete from hr_payslip_input where contract_id=%s and code=%s"
        cr.execute(sql, (contracts.id, 'INPUT_ABS_07'))

        sql = """select count(*) from aag_absensi_aag_absensi where idno=%s and month=%s and year=%s and code=%s"""
        month = date_from.month 
        year = date_from.year
        cr.execute(sql, (contracts.employee_id.x_idno, month, year, 7))
        result = cr.fetchone()
        if result:
            amount = result[0]

        res.append({
            'name': 'Absensi 07-Cuti Hamil',
            'code': 'INPUT_ABS_07',
            'amount': amount,
            'contract_id': contracts.id 
        })
#=======================================
# HITUNG CUTI MELAHIRKAN (08)
#=======================================
        cr = self.env.cr 
        sql = "delete from hr_payslip_input where contract_id=%s and code=%s"
        cr.execute(sql, (contracts.id, 'INPUT_ABS_08'))

        sql = """select count(*) from aag_absensi_aag_absensi where idno=%s and month=%s and year=%s and code=%s"""
        month = date_from.month 
        year = date_from.year
        cr.execute(sql, (contracts.employee_id.x_idno, month, year, 8))
        result = cr.fetchone()
        if result:
            amount = result[0]

        res.append({
            'name': 'Absensi 08-Cuti Melahirkan',
            'code': 'INPUT_ABS_08',
            'amount': amount,
            'contract_id': contracts.id 
        })

#=======================================
# HITUNG CUTI BERSAMA (18)
#=======================================
        cr = self.env.cr 
        sql = "delete from hr_payslip_input where contract_id=%s and code=%s"
        cr.execute(sql, (contracts.id, 'INPUT_ABS_08'))

        sql = """select count(*) from aag_absensi_aag_absensi where idno=%s and month=%s and year=%s and code=%s"""
        month = date_from.month 
        year = date_from.year
        cr.execute(sql, (contracts.employee_id.x_idno, month, year, 18))
        result = cr.fetchone()
        if result:
            amount = result[0]

        res.append({
            'name': 'Absensi 18-Cuti Bersama',
            'code': 'INPUT_ABS_18',
            'amount': amount,
            'contract_id': contracts.id 
        })
#=======================================
# HITUNG SISA CUTI BULAN LALU ()
#=======================================
        cr = self.env.cr 
        sql = "delete from hr_payslip_input where contract_id=%s and code=%s"
        cr.execute(sql, (contracts.id, 'INPUT_LEAVE_PRVBAL'))

        sql = """select x_end from aag_leave_master_aag_leave_master where x_idno=%s and status=%s"""
        cr.execute(sql, (contracts.employee_id.x_idno, 'True'))
        result = cr.fetchone()
        if result:
            amount = result[0]

        res.append({
            'name': 'Sisa Cuti Bulan Lalu',
            'code': 'INPUT_LEAVE_PRVBAL',
            'amount': amount,
            'contract_id': contracts.id 
        })
#=============================

        return res         
