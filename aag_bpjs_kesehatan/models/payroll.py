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
        
        cr = self.env.cr 
        sql = "delete from hr_payslip_input where contract_id=%s and code=%s"
        cr.execute(sql, (self.contract_id.id, 'INPUT_BPJSKES_EMP'))

        sql = """select amount_dtk from aag_bpjs_kesehatan_aag_bpjs_kesehatan where idno=%s and month=%s and year=%s"""
        month = self.date_from.month 
        year = self.date_from.year 
        cr.execute(sql, (self.employee_id.x_idno, month, year))
        result = cr.fetchone()
        if result:
            amount = result[0]

        res.append({
            'name': 'BPJS-Kes DTK',
            'code': 'INPUT_BPJSKES_EMP',
            'amount': amount,
            'contract_id': self.contract_id.id 
        })

        amount = 0
        
        cr = self.env.cr 
        sql = "delete from hr_payslip_input where contract_id=%s and code=%s"
        cr.execute(sql, (self.contract_id.id, 'INPUT_BPJSKES_COM'))

        sql = """select amount_dtp from aag_bpjs_kesehatan_aag_bpjs_kesehatan where idno=%s and month=%s and year=%s"""
        month = self.date_from.month 
        year = self.date_from.year 
        cr.execute(sql, (self.employee_id.x_idno, month, year))
        result = cr.fetchone()
        if result:
            amount = result[0]

        res.append({
            'name': 'BPJS-Kes DTP',
            'code': 'INPUT_BPJSKES_COM',
            'amount': amount,
            'contract_id': self.contract_id.id 
        })

        return res         
