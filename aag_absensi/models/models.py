# -*- coding: utf-8 -*-

from odoo import models, fields, api


class aag_absensi(models.Model):
    _name = 'aag_absensi.aag_absensi'
    _description = 'aag_absensi.aag_absensi'

    idno = fields.Integer('IDNO')
    date = fields.Date('Date')
    month = fields.Integer('Month')
    year = fields.Integer('Year')    
    code = fields.Integer('Code')
    remark = fields.Char('Remark')
    status = fields.Boolean('Status')

class aag_leave_master(models.Model):
    _name = 'aag_leave_master.aag_leave_master'
    _description = 'aag_leave_master.aag_leave_master'

    x_idno = fields.Integer('IDNO')
    x_begper = fields.Date('Start Period')
    x_endper = fields.Date('End Period')
    x_beg = fields.Float('Beginning')
    x_use = fields.Float('Usage')    
    x_end = fields.Float('Ending')

    x_code01 = fields.Integer('Annual Leave')
    x_code02 = fields.Integer('Special Leave-1')
    x_code03 = fields.Integer('Celebration')
    x_code04 = fields.Integer('Menstruation')
    x_code05 = fields.Integer('Sick Leave')
    x_code06 = fields.Integer('Absent')
    x_code07 = fields.Integer('Pregnancy Leave')
    x_code08 = fields.Integer('Birth Leave')
    x_code11 = fields.Integer('Annual Leave/2')
    x_code17 = fields.Integer('Condolence Leave')
    x_code18 = fields.Integer('Mass Leave')
    x_code21 = fields.Integer('Official Leave')
    x_code25 = fields.Integer('At-Home')
    x_code35 = fields.Integer('Work From Home')
    x_code46 = fields.Integer('Late-In')
    x_code56 = fields.Integer('Early-Out')
    x_code66 = fields.Integer('Private-Out')

    x_ycode01 = fields.Integer('YTD Annual Leave')
    x_ycode02 = fields.Integer('YTD Special Leave-1')
    x_ycode03 = fields.Integer('YTD Celebration')
    x_ycode04 = fields.Integer('YTD Menstruation')
    x_ycode05 = fields.Integer('YTD Sick Leave')
    x_ycode06 = fields.Integer('YTD Absent')
    x_ycode07 = fields.Integer('YTD Pregnancy Leave')
    x_ycode08 = fields.Integer('YTD Birth Leave')
    x_ycode11 = fields.Integer('YTD Annual Leave/2')
    x_ycode17 = fields.Integer('YTD Condolence Leave')
    x_ycode18 = fields.Integer('YTD Mass Leave')
    x_ycode21 = fields.Integer('YTD Official Leave')
    x_ycode25 = fields.Integer('YTD At-Home')
    x_ycode35 = fields.Integer('YTD Work From Home')
    x_ycode46 = fields.Integer('YTD Late-In')
    x_ycode56 = fields.Integer('YTD Early-Out')
    x_ycode66 = fields.Integer('YTD Private-Out')

    x_prev_beg = fields.Float('Prev. Beginning')
    x_prev_use = fields.Float('Prev. Usage')
    x_prev_end = fields.Float('Prev. Ending')
    x_prev_ovr = fields.Float('Prev. Overlimit')

    status = fields.Boolean('Status')
