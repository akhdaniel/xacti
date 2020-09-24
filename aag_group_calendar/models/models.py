# -*- coding: utf-8 -*-

from odoo import models, fields, api


class aag_group_calendar(models.Model):
    _name = 'aag_group_calendar.aag_group_calendar'
    _description = 'aag_group_calendar.aag_group_calendar'

    month = fields.Integer('Month')
    year = fields.Integer('Year')

    x_wrkgrp = fields.Char('Work Group')
    x_prev_str = fields.Date('Start Prev. Month')
    x_prev_end = fields.Date('End Prev. Month')
    x_curr_str = fields.Date('Start Curr. Month')
    x_curr_end = fields.Date('End Curr. Month')
    x_twd_1st = fields.Integer('1st Half Working Day')
    x_twd_2nd = fields.Integer('2nd Half Working Day')
    x_hol01 = fields.Date('Holiday-01')
    x_hol02 = fields.Date('Holiday-02')
    x_hol03 = fields.Date('Holiday-03')
    x_hol04 = fields.Date('Holiday-04')
    x_hol05 = fields.Date('Holiday-05')
    x_hol06 = fields.Date('Holiday-06')
    x_hol07 = fields.Date('Holiday-07')
    x_hol08 = fields.Date('Holiday-08')
    x_hol09 = fields.Date('Holiday-09')
    x_hol10 = fields.Date('Holiday-10')
    x_hol11 = fields.Date('Holiday-11')
    x_hol12 = fields.Date('Holiday-12')
    x_hol13 = fields.Date('Holiday-13')
    x_hol14 = fields.Date('Holiday-14')
    x_hol15 = fields.Date('Holiday-15')
    x_hol16 = fields.Date('Holiday-16')
    x_hol17 = fields.Date('Holiday-17')
    x_hol18 = fields.Date('Holiday-18')
    x_hol19 = fields.Date('Holiday-19')
    x_hol20 = fields.Date('Holiday-20')
    x_hol21 = fields.Date('Holiday-21')
    x_hol22 = fields.Date('Holiday-22')
    x_hol23 = fields.Date('Holiday-23')
    x_hol24 = fields.Date('Holiday-24')
    x_hol25 = fields.Date('Holiday-25')
    x_hol26 = fields.Date('Holiday-26')
    x_hol27 = fields.Date('Holiday-27')
    x_hol28 = fields.Date('Holiday-28')
    x_hol29 = fields.Date('Holiday-29')
    x_hol30 = fields.Date('Holiday-30')
    x_hol31 = fields.Date('Holiday-31')
    status = fields.Boolean('Status')