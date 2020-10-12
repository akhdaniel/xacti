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
        cr.execute(sql, (contracts.id, 'INPUT_ACCGRS'))

        sql = """select x_accgrs from aag_pph_accumulation_aag_pph_accumulation where idno=%s and x_accmm=%s"""
        month = date_to.month 
        year = date_to.year 
        cr.execute(sql, (contracts.employee_id.x_idno, month))
        result = cr.fetchone()
        if result:
            amount = result[0]

        res.append({
            'name': 'Other Income',
            'code': 'INPUT_ACCGRS',
            'amount': amount,
            'contract_id': contracts.id 
        })

        return res         