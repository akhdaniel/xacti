# -*- coding: utf-8 -*-

from odoo import models, fields, api


class aag_koperasi(models.Model):
    _name = 'aag_koperasi.aag_koperasi'
    _description = 'aag_koperasi.aag_koperasi'

    # name = fields.Char('NIK')
    idno = fields.Integer('IDNO')
    amount = fields.Float('Potongan')
    remark = fields.Char('Remark')
    month = fields.Integer('Month')
    year = fields.Integer('Year')
    status = fields.Boolean('Status')
    basic = fields.Integer('Gaji Pokok')
    trans = fields.Integer('Transport')

    header_id = fields.Many2one(string='Header', comodel_name='aag_koperasi.aag_koperasi_header')

class aag_koperasi_header(models.Model):
    _name = 'aag_koperasi.aag_koperasi_header'
    _description = 'aag_koperasi.aag_koperasi_header'

    # name = fields.Char('NIK')
    month = fields.Integer('Month')
    year = fields.Integer('Year')
    state = fields.Selection(string='Status', selection=[('draft', 'Draft'), ('open', 'Dlm Proses'), ('done', 'Verified')])
    detail_ids = fields.One2many(string='Data Detail', comodel_name='aag_koperasi.aag_koperasi', inverse_name='header_id')

    def button_confirm(self):
        cr = self.env.cr 
        sql = '''update aag_koperasi_aag_koperasi as kop set basic=(
            select contract.wage+contract.x_occup+contract.x_family+contract.x_functional+contract.x_other from hr_contract contract
            join hr_employee emp on contract.employee_id=emp.id
            where emp.x_idno=kop.idno 
        ) where header_id=%s'''
        cr.execute(sql, (self.id,))

        sql = '''update aag_koperasi_aag_koperasi as kop set trans=(
            select 21*contract.x_trans from hr_contract contract
            join hr_employee emp on contract.employee_id=emp.id
            where emp.x_idno=kop.idno and emp.x_class='WK'
        ) where header_id=%s'''
        cr.execute(sql, (self.id,))

        sql = '''update aag_koperasi_aag_koperasi as kop set trans=(
            select contract.x_trans from hr_contract contract
            join hr_employee emp on contract.employee_id=emp.id
            where emp.x_idno=kop.idno and emp.x_class<>'WK'
        ) where header_id=%s'''
        cr.execute(sql, (self.id,))

        sql = '''update aag_koperasi_aag_koperasi as kop set status=
        case
            when amount>(basic+trans)*0.3 then false
            else true            
        end
         where header_id=%s'''
        cr.execute(sql, (self.id,))


        self.state='open'
    def button_verification(self):
        self.state='done'
    def button_cancel(self):
        self.state='draft'
    


