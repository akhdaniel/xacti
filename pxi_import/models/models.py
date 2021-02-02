# -*- coding: utf-8 -*-

from odoo import models, fields, api

class pxi_import(models.Model):
    _name = 'pxi_import.pxi_import'
    _description = 'pxi_import.pxi_import'

    x_idno = fields.Integer('IDNO')
    remark1 = fields.Char('Remark-1')
    remark2 = fields.Char('Remark-2')
    remark3 = fields.Char('Remark-3')
    remark4 = fields.Char('Remark-4')
    remark5 = fields.Char('Remark-5')

    amount1 = fields.Integer('Amount-1')
    amount2 = fields.Integer('Amount-2')
    amount3 = fields.Integer('Amount-3')
    amount4 = fields.Integer('Amount-4')
    amount5 = fields.Integer('Amount-5')

    desimal1 = fields.Float('Desimal-1')
    desimal2 = fields.Float('Desimal-2')
    desimal3 = fields.Float('Desimal-3')
    desimal4 = fields.Float('Desimal-4')
    desimal5 = fields.Float('Desimal-5')

    status1 = fields.Boolean('Status-1')
    status2 = fields.Boolean('Status-2')
    status3 = fields.Boolean('Status-3')
