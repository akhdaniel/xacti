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
    
    def hitung_reimburse_ytd(self):
        cr=self.env.cr
        sql='''update aag_medical_master_aag_medical_master set ytdamt=ytdamt+
        (select total from hr_payslip_line where code='I_MEDICAL' and slip_id=%s)
        where idno=%s'''
        _logger.info(sql,self.id,self.employee_id.x_idno)
        cr.execute(sql,(self.id,self.employee_id.x_idno))

    def action_payslip_done(self):
        res = super(hr_payslip, self).action_payslip_done()
        _logger.info('Action payslip done')
        self.hitung_reimburse_ytd()

        return res
class hr_payslip_run(models.Model):
    _name = 'hr.payslip.run'
    _inherit = 'hr.payslip.run'

    def close_payslip_run(self):
        res = super(hr_payslip_run, self).close_payslip_run()
        _logger.info('Close payslip run')
        for payslip in self.slip_ids:
            payslip.action_payslip_done()
        return res        


