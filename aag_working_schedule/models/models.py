# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class aag_work_schedule(models.Model):
    _name = 'work_schedule.work_schedule'
    _description = 'work_schedule.work_schedule'

    x_year = fields.Integer('Year')
    x_month = fields.Integer('Monht')
    x_wrkgrp = fields.Char('Work Group')
    x_day01 = fields.Integer('Day-01')
    x_day02 = fields.Integer('Day-02')
    x_day03 = fields.Integer('Day-03')
    x_day04 = fields.Integer('Day-04')
    x_day05 = fields.Integer('Day-05')
    x_day06 = fields.Integer('Day-06')
    x_day07 = fields.Integer('Day-07')
    x_day08 = fields.Integer('Day-08')
    x_day09 = fields.Integer('Day-09')
    x_day10 = fields.Integer('Day-10')
    x_day11 = fields.Integer('Day-11')
    x_day12 = fields.Integer('Day-12')
    x_day13 = fields.Integer('Day-13')
    x_day14 = fields.Integer('Day-14')
    x_day15 = fields.Integer('Day-15')
    x_day16 = fields.Integer('Day-16')
    x_day17 = fields.Integer('Day-17')
    x_day18 = fields.Integer('Day-18')
    x_day19 = fields.Integer('Day-19')
    x_day20 = fields.Integer('Day-20')
    x_day21 = fields.Integer('Day-21')
    x_day22 = fields.Integer('Day-22')
    x_day23 = fields.Integer('Day-23')
    x_day24 = fields.Integer('Day-24')
    x_day25 = fields.Integer('Day-25')
    x_day26 = fields.Integer('Day-26')
    x_day27 = fields.Integer('Day-27')
    x_day28 = fields.Integer('Day-28')
    x_day29 = fields.Integer('Day-29')
    x_day30 = fields.Integer('Day-30')
    x_day31 = fields.Integer('Day-31')
    x_lasrot = fields.Char('Last Rotation')

    def cron_update_contract(self):
        _logger.info('Jalankan Cron Update Kontrak')
