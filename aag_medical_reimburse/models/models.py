# -*- coding: utf-8 -*-

from odoo import models, fields, api


class aag_medical_reimburse(models.Model):
    _name = 'aag_medical_reimburse.aag_medical_reimburse'
    _description = 'aag_medical_reimburse.aag_medical_reimburse'

    idno = fields.Integer('IDNO')
    trndat = fields.Date('Trans. Date')
    cata = fields.Char('Category')
    medcod = fields.Char('Med-Code')
    patien = fields.Char('Patien')
    dr = fields.Char('Hospital/Docter')
    apotik = fields.Char('Apotik')
    medamt = fields.Integer('Med-Amount')
    remark = fields.Char('Remark')
    paydat = fields.Date('Payment Date')
    month = fields.Integer('Month')
    year = fields.Integer('Year')
    status = fields.Boolean('Status')
    flag1 = fields.Char('Flag-1')
    flag2 = fields.Char('Flag-2')
    flag3 = fields.Char('Flag-3')
    flag4 = fields.Char('Flag-4')
    header_id = fields.Many2one(string='Header', comodel_name='aag_medical_reimburse.aag_medical_reimburse_header')


class aag_medical_reimburse_header(models.Model):
    _name = 'aag_medical_reimburse.aag_medical_reimburse_header'
    _description = 'aag_medical_reimburse.aag_medical_reimburse_header'

    # name = fields.Char('NIK')
    month = fields.Integer('Month')
    year = fields.Integer('Year')
    state = fields.Selection(string='Status', selection=[('draft', 'Draft'), ('open', 'Dlm Proses'), ('done', 'Verified')])
    detail_ids = fields.One2many(string='Data Detail', comodel_name='aag_medical_reimburse.aag_medical_reimburse', inverse_name='header_id')

    def button_confirm(self):
        cr = self.env.cr 
        sql = '''update aag_medical_reimburse_aag_medical_reimburse as reimburse set status=
        case
            when amount<0 then false
            else true            
        end
         where header_id=%s'''
        cr.execute(sql, (self.id,))

        self.state='open'
    def button_verification(self):
        self.state='done'
    def button_cancel(self):
        self.state='draft'


class aag_medical_master(models.Model):
    _name = 'aag_medical_master.aag_medical_master'
    _description = 'aag_medical_master.aag_medical_master'

    idno = fields.Integer('IDNO')
    allow = fields.Integer('Allowance')
    ytdamt = fields.Integer('YTD Reimbursement')
    curamt = fields.Integer('Last Reimbursement')
    active = fields.Boolean('Active')
    spouse = fields.Char('Spouse Name')
    child1 = fields.Char('Child Name-1')
    child2 = fields.Char('Child Name-2')
    child3 = fields.Char('Child Name-3')
    child4 = fields.Char('Child Name-4')
    child5 = fields.Char('Child Name-5')
    child6 = fields.Char('Child Name-6')
    child7 = fields.Char('Child Name-7')
