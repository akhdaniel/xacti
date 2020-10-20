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

class aag_dept_group_pf015(models.Model):
    _name = 'aag_dept_group_pf015.aag_dept_group_pf015'
    _description = 'aag_dept_group_pf015.aag_dept_group_pf015'

    x_lncode= fields.Integer('Line Code')
    x_lndesc= fields.Char('Group Name')
    x_comp01= fields.Integer('Dept_Sect-01')
    x_comp02= fields.Integer('Dept_Sect-02')
    x_comp03= fields.Integer('Dept_Sect-03')
    x_comp04= fields.Integer('Dept_Sect-04')
    x_comp05= fields.Integer('Dept_Sect-05')
    x_comp06= fields.Integer('Dept_Sect-06')
    x_comp07= fields.Integer('Dept_Sect-07')
    x_comp08= fields.Integer('Dept_Sect-08')
    x_comp09= fields.Integer('Dept_Sect-09')
    x_comp10= fields.Integer('Dept_Sect-10')
    x_comp11= fields.Integer('Dept_Sect-11')
    x_comp12= fields.Integer('Dept_Sect-12')
    x_comp13= fields.Integer('Dept_Sect-13')
    x_comp14= fields.Integer('Dept_Sect-14')
    x_comp15= fields.Integer('Dept_Sect-15')
    x_comp16= fields.Integer('Dept_Sect-16')
    x_comp17= fields.Integer('Dept_Sect-17')
    x_comp18= fields.Integer('Dept_Sect-18')
    x_comp19= fields.Integer('Dept_Sect-19')
    x_comp20= fields.Integer('Dept_Sect-20')
    x_comp21= fields.Integer('Dept_Sect-21')
    x_comp22= fields.Integer('Dept_Sect-22')
    x_comp23= fields.Integer('Dept_Sect-23')
    x_comp24= fields.Integer('Dept_Sect-24')
    x_comp25= fields.Integer('Dept_Sect-25')
    x_comp26= fields.Integer('Dept_Sect-26')
    x_comp27= fields.Integer('Dept_Sect-27')
    x_comp28= fields.Integer('Dept_Sect-28')
    x_comp29= fields.Integer('Dept_Sect-29')
    x_comp30= fields.Integer('Dept_Sect-30')


