# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import time

class aag_work_schedule(models.Model):
    _name = 'work_schedule.work_schedule'
    _description = 'work_schedule.work_schedule'

    x_year = fields.Integer('Year')
    x_month = fields.Integer('Month')
    x_wrkgrp = fields.Char('Work Group')
    x_day01 = fields.Char('Day-01')
    x_day02 = fields.Char('Day-02')
    x_day03 = fields.Char('Day-03')
    x_day04 = fields.Char('Day-04')
    x_day05 = fields.Char('Day-05')
    x_day06 = fields.Char('Day-06')
    x_day07 = fields.Char('Day-07')
    x_day08 = fields.Char('Day-08')
    x_day09 = fields.Char('Day-09')
    x_day10 = fields.Char('Day-10')
    x_day11 = fields.Char('Day-11')
    x_day12 = fields.Char('Day-12')
    x_day13 = fields.Char('Day-13')
    x_day14 = fields.Char('Day-14')
    x_day15 = fields.Char('Day-15')
    x_day16 = fields.Char('Day-16')
    x_day17 = fields.Char('Day-17')
    x_day18 = fields.Char('Day-18')
    x_day19 = fields.Char('Day-19')
    x_day20 = fields.Char('Day-20')
    x_day21 = fields.Char('Day-21')
    x_day22 = fields.Char('Day-22')
    x_day23 = fields.Char('Day-23')
    x_day24 = fields.Char('Day-24')
    x_day25 = fields.Char('Day-25')
    x_day26 = fields.Char('Day-26')
    x_day27 = fields.Char('Day-27')
    x_day28 = fields.Char('Day-28')
    x_day29 = fields.Char('Day-29')
    x_day30 = fields.Char('Day-30')
    x_day31 = fields.Char('Day-31')
    x_lasrot = fields.Char('Last Rotation')

    def cron_update_contract(self):
        _logger.info('Jalankan Cron Update Kontrak')

        field_day = 'x_day%02s'  % time.strftime("%d")
        _logger.info('field_day=%s', field_day)

        year = time.strftime("%Y")
        month = time.strftime("%m")
        month = 10
        sql = """
        update hr_contract con set resource_calendar_id = (
            select id from resource_calendar where name = emp.x_wrkgrp || '-' || (select """+field_day+""" from work_schedule_work_schedule where x_year=%s and x_month=%s and x_wrkgrp=emp.x_wrkgrp)
        ) 
        from hr_employee emp
        where emp.id = con.employee_id and emp.x_wrkgrp='A0' and emp.x_empsts <> 'T'
        """

        self.env.cr.execute(sql, (year, month))
