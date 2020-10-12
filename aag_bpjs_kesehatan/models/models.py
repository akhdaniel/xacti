# -*- coding: utf-8 -*-

from odoo import models, fields, api


class aag_bpjs_kesehatan(models.Model):
    _name = 'aag_bpjs_kesehatan.aag_bpjs_kesehatan'
    _description = 'aag_bpjs_kesehatan.aag_bpjs_kesehatan'

    idno = fields.Integer('IDNO')
    
    amount_dtk = fields.Integer('BPJS-Kes DTK')
    amount_dtp = fields.Integer('BPJS-Kes DTP')
    code = fields.Char('Code')
    remark = fields.Char('Remark')
    month = fields.Integer('Month')
    year = fields.Integer('Year')
    status = fields.Boolean('Status')
    header_id = fields.Many2one(string='Header', comodel_name='aag_bpjs_kesehatan.aag_bpjs_kesehatan_header')

class aag_bpjs_kesehatan_header(models.Model):
    _name = 'aag_bpjs_kesehatan.aag_bpjs_kesehatan_header'
    _description = 'aag_bpjs_kesehatan.aag_bpjs_kesehatan_header'

    # name = fields.Char('NIK')
    month = fields.Integer('Month')
    year = fields.Integer('Year')
    state = fields.Selection(string='Status', selection=[('draft', 'Draft'), ('open', 'Dlm Proses'), ('done', 'Verified')])
    detail_ids = fields.One2many(string='Data Detail', comodel_name='aag_bpjs_kesehatan.aag_bpjs_kesehatan', inverse_name='header_id')

    def button_confirm(self):
        cr = self.env.cr 
        sql = '''update aag_bpjs_kesehatan_aag_bpjs_kesehatan as bpjs_kes set status=
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