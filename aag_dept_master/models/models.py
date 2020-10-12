# -*- coding: utf-8 -*-

from odoo import models, fields, api


class aag_dept_master(models.Model):
    _name = 'aag_dept_master.aag_dept_master'
    _description = 'aag_dept_master.aag_dept_master'

    x_dept= fields.Integer('Dept Code')
    x_sect= fields.Integer('Section Code')
    x_sbsec= fields.Integer('Sub-Section Code')
    x_desc= fields.Char('Dept/Section Name')
    x_group= fields.Char('Dept Group')
    x_direct= fields.Boolean('Direct')

class aag_dept_group(models.Model):
    _name = 'aag_dept_group.aag_dept_group'
    _description = 'aag_dept_group.aag_dept_group'

    x_dept= fields.Integer('Dept Code')
    x_sdesc= fields.Char('Short Description')
    x_ldesc= fields.Char('Long Description')
    x_group1= fields.Char('Group-1')
    x_group2= fields.Char('Group-2')
    x_group3= fields.Char('Group-3')
    x_group4= fields.Char('Group-4')
