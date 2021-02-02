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
        input_income_01 = 'INPUT_INCOME_01'
        amount = self.get_income_code(input_income_01,'01', contracts, date_from, date_to)
        res.append({
            'name': 'Other Income 01-Gaji Pokok',
            'code': input_income_01,
            'amount': amount,
            'contract_id': contracts.id 
        })     

        amount = 0        
        input_income_04 = 'INPUT_INCOME_04'
        amount = self.get_income_code(input_income_04,'04', contracts, date_from, date_to)
        res.append({
            'name': 'Other Income 04-Medical',
            'code': input_income_04,
            'amount': amount,
            'contract_id': contracts.id 
        })     

        amount = 0        
        input_income_05 = 'INPUT_INCOME_05'
        amount = self.get_income_code(input_income_05,'05', contracts, date_from, date_to)
        res.append({
            'name': 'Other Income 05-Transport',
            'code': input_income_05,
            'amount': amount,
            'contract_id': contracts.id
        })

        amount = 0        
        input_income_07 = 'INPUT_INCOME_07'
        amount = self.get_income_code(input_income_07,'07', contracts, date_from, date_to)
        res.append({
            'name': 'Other Income 07-Lembur',
            'code': input_income_07,
            'amount': amount,
            'contract_id': contracts.id 
        })

        amount = 0        
        input_income_08 = 'INPUT_INCOME_08'
        amount = self.get_income_code(input_income_08,'08', contracts, date_from, date_to)
        res.append({
            'name': 'Other Income 08-Lain Lain',
            'code': input_income_08,
            'amount': amount,
            'contract_id': contracts.id 
        })

        amount = 0        
        input_income_09 = 'INPUT_INCOME_09'
        amount = self.get_income_code(input_income_09,'09', contracts, date_from, date_to)
        res.append({
            'name': 'Other Income 09-Uang Makan',
            'code': input_income_09,
            'amount': amount,
            'contract_id': contracts.id 
        })

        amount = 0        
        input_income_10 = 'INPUT_INCOME_10'
        amount = self.get_income_code(input_income_10,'10', contracts, date_from, date_to)
        res.append({
            'name': 'Other Income 10-Tunj. Shift',
            'code': input_income_10,
            'amount': amount,
            'contract_id': contracts.id 
        })

#        amount = 0        
#        input_income_91 = 'INPUT_MED_ALLOW'
#        amount = self.get_income_code(input_income_91,'91', contracts, date_from, date_to)
#        res.append({
#            'name': 'Medical Allowance 91',
#            'code': input_income_91,
#            'amount': amount,
#            'contract_id': contracts.id 
#        })

#        amount = 0        
#        input_income_92 = 'INPUT_MED_PRVYTD'
#        amount = self.get_income_code(input_income_92,'92', contracts, date_from, date_to)
#        res.append({
#            'name': 'Medical Prev YTD Reimburse 92',
#            'code': input_income_92,
#            'amount': amount,
#            'contract_id': contracts.id 
#        })

        amount = 0        
        input_income_95 = 'INPUT_PPH_DTP'
        amount = self.get_income_code(input_income_95,'95', contracts, date_from, date_to)
        res.append({
            'name': 'PPh21 DTP 95',
            'code': input_income_95,
            'amount': amount,
            'contract_id': contracts.id 
        })

        # amount = 0        
        # input_income_97 = 'INPUT_LEAVE_PRVBAL'
        # amount = self.get_income_code(input_income_97,'97', contracts, date_from, date_to)
        # res.append({
        #     'name': 'Leave Prev Balance',
        #     'code': input_income_97,
        #     'amount': amount,
        #     'contract_id': contracts.id 
        # })


        return res

    def get_income_code(self, input_code, code, contracts, date_from, date_to):
        cr = self.env.cr 
        sql = "delete from hr_payslip_input where contract_id=%s and code=%s"
        cr.execute(sql, (contracts.id, input_code))

        sql = """select sum(amount) from aag_other_income_aag_other_income where idno=%s and month=%s and year=%s and code=%s"""
        month = date_to.month 
        year = date_to.year 
        cr.execute(sql, (contracts.employee_id.x_idno, month, year, code))
        result = cr.fetchone()
        if result:
            amount = result[0]   
        return amount      

    #=========================================


