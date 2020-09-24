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
#    def get_inputs(self, contracts, date_from, date_to):
    def get_inputs(self, contracts, date_from, date_to):

        res = super(hr_payslip, self).get_inputs(contracts, date_from, date_to)

        amount = 0        
        input_twd_01 = 'INPUT_TWD'
        amount = self.get_input_code_twd(input_twd_01)
        res.append({
            'name': 'Total Working Day',
            'code': input_twd_01,
            'amount': amount,
            'contract_id': self.contract_id.id 
        })     

        return res

    def get_input_code_twd(self, input_code):
        cr = self.env.cr 
        sql = "delete from hr_payslip_input where contract_id=%s and code=%s"
        cr.execute(sql, (self.contract_id.id, input_code))

        sql = """select x_twd_1st+x_twd_2nd from aag_group_calendar_aag_group_calendar where x_wrkgrp=%s and month=%s and year=%s"""
        month = self.date_to.month 
        year = self.date_to.year 
        cr.execute(sql, (self.employee_id.x_wrkgrp, month, year))
        result = cr.fetchone()
        if result:
            amount = result[0]   
        return amount      
