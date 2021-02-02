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
# GET MEDICAL REIMBURSE
#=======================================
        cr = self.env.cr 
        sql = "delete from hr_payslip_input where contract_id=%s and code=%s"
        cr.execute(sql, (contracts.id, 'INPUT_MEDICAL'))

        sql = """select sum(medamt) from aag_medical_reimburse_aag_medical_reimburse where idno=%s and month=%s and year=%s and medcod <>%s"""
        month = date_to.month 
        year = date_to.year 
        cr.execute(sql, (contracts.employee_id.x_idno, month, year,'C'))
        result = cr.fetchone()
        if result:
            amount = result[0]

        res.append({
            'name': 'Medical Reimburse',
            'code': 'INPUT_MEDICAL',
            'amount': amount,
            'contract_id': contracts.id 
        })

#=======================================
# GET MEDICAL ALLOWANCE USAGE 
#=======================================
        cr = self.env.cr 
        sql = "delete from hr_payslip_input where contract_id=%s and code=%s"
        cr.execute(sql, (contracts.id, 'INPUT_MED_ALWUSG'))

        sql = """select sum(medamt) from aag_medical_reimburse_aag_medical_reimburse where idno=%s and month=%s and year=%s and medcod <>%s"""
        month = date_to.month 
        year = date_to.year 
        cr.execute(sql, (contracts.employee_id.x_idno, month, year,'I'))
        result = cr.fetchone()
        if result:
            amount = result[0]

        res.append({
            'name': 'Medical Allowance Usage',
            'code': 'INPUT_MED_ALWUSG',
            'amount': amount,
            'contract_id': contracts.id 
        })
#=======================================
# GET MEDICAL ALLOWANCE
#=======================================
        cr = self.env.cr 
        sql = "delete from hr_payslip_input where contract_id=%s and code=%s"
        cr.execute(sql, (contracts.id, 'INPUT_MED_ALLOW'))
        sql = """select allow from aag_medical_master_aag_medical_master where idno=%s and active=%s"""
        cr.execute(sql, (contracts.employee_id.x_idno, 'True'))
        result = cr.fetchone()
        if result:
             amount = result[0]

        res.append({
            'name': 'Medical Allowance',
            'code': 'INPUT_MED_ALLOW',
            'amount': amount,
            'contract_id': contracts.id 
        })

#=======================================
# GET MEDICAL PREV-YTD REIMBURSE
#=======================================
        cr = self.env.cr 
        sql = "delete from hr_payslip_input where contract_id=%s and code=%s"
        cr.execute(sql, (contracts.id, 'INPUT_MED_PRVYTD'))
        sql = """select ytdamt from aag_medical_master_aag_medical_master where idno=%s and active=%s"""
        cr.execute(sql, (contracts.employee_id.x_idno, 'True'))
        result = cr.fetchone()
        if result:
            amount = result[0]

        res.append({
            'name': 'Medical Prev. YTD Reimburse',
            'code': 'INPUT_MED_PRVYTD',
            'amount': amount,
            'contract_id': contracts.id 
        })

        return res

