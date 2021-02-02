# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date

import logging
_logger = logging.getLogger(__name__)
import xlsxwriter

import base64
from io import BytesIO
# from io import StringIO

class report_emp_active_01_header(models.Model):
    _name = 'aag.report_emp_active_01_header'
    _description = 'report emp_active_01 header'

    name = fields.Char("Name")
    day = fields.Char("Day")
    month = fields.Integer("Month")
    year = fields.Integer("Year")
    exclude = fields.Char("Exclude")

    export_file = fields.Binary("Export File")
    export_filename = fields.Char(string="Export File Name",  )

    detail_ids = fields.One2many(comodel_name="aag.report_emp_active_01_detail", inverse_name="header_id")

    def action_generate(self):
        cr = self.env.cr

        sql = "delete from aag_report_emp_active_01_detail where header_id=%s"
        cr.execute(sql, (self.id,))

        sql = """
            INSERT INTO aag_report_emp_active_01_detail (
                header_id,
                "IDNO",
                "NAME",
                "GENDER",
                "DATBIR",
                "PLACE",
                "MARSTS",
                "EDUC",
                "DEPT",
                "SECT",
                "SBSEC",
                "DESC",
                "ALLCD",
                "WRKGRP",
                "ADDRESS",
                "EMPSTS",
                "DATENT",
                "STSCNT",
                "STRDAT",
                "ENDDAT",
                "TERDAT",
                "POSIT",
                "DIRECT",
                "PHONE",
                "CLASS",
                "RELIGION",
                "SPMI",
                "KTPNO",
                "BPJSTK_ID",
                "BPJSKES_ID",
                "NPWP",
                "ACC_NUMBER",
                "ACC_NAME",
                "GROUP_1",
                "GROUP_2",
                "GROUP_3",
                "GROUP_4"                
            ) 
            SELECT 
                %s,
                emp.x_idno, 
                emp.name, 
                emp.gender as GENDER, 
                emp.birthday as DATBIR,
                emp.place_of_birth as PLACE,
                emp.marital as MARSTS,
                emp.certificate as EDUC,
                emp.x_dept as DEPT,
                emp.x_sect as SECT,
                emp.x_sbsec as SBSEC,
                dept.x_desc as DESC,
                emp.x_allcd as ALLCD,
                emp.x_wrkgrp as WRKGRP,
                emp.address_home_id as ADDRESS,
                emp.x_empsts as EMPSTS,
                con.date_start as ENTDAT,
                emp.x_empsts as STSCNT,
                con.date_start as STRDAT,
                con.date_end as ENDDAT,
                con.date_end as DATTER,
                job.name as POSIT,
                emp.x_direct as DIRECT,
                emp.mobile_phone as PHONE,
                emp.x_class as CLASS,
                emp.x_religion as RELIGION,
                emp.x_spmi as SPMI,
                emp.identification_id KTPNO,
                emp.x_nobpjstk as BPJSTK_ID,
                emp.x_nobpjskes as BPJSKES_ID,
                emp.x_npwp as NPWP,
                emp.x_accno as ACC_NUMBER,
                emp.x_accname as ACC_NAME,
                grp.x_group1 as GROUP_1,
                grp.x_group2 as GROUP_2,
                grp.x_group3 as GROUP_3,
                grp.x_group4 as GROUP_4  
            from 
                hr_employee emp
            join 
                hr_contract con on emp.id = con.employee_id
            join 
                aag_dept_master_aag_dept_master dept on dept.x_dept = emp.x_dept
                and dept.x_sect = emp.x_sect
                and dept.x_sbsec = emp.x_sbsec
            join 
                hr_job job on emp.job_id = job.id
            join 
                aag_dept_group_aag_dept_group grp on emp.x_dept = grp.x_dept                
            where
                emp.x_empsts <> %s and emp.x_empsts <> 'A'
        """
        self.exclude = 'T'
        cr.execute(sql, (self.id, self.exclude))


    def action_export(self):
        file_data = BytesIO()
        workbook = xlsxwriter.Workbook(file_data)
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        font12 = workbook.add_format({'bold': True, 'font_size': 12})
        font14 = workbook.add_format({'bold': True, 'font_size': 14})
        numeric = workbook.add_format({'num_format': '#,##0'})
        # numeric2 = workbook.add_format({'num_format': '#,##0.00'})
        date = workbook.add_format({'num_format': 'd mmm yyyy'})

        # SET COLUMN WIDTH
        worksheet.set_column('B:B', 6)  # Column  B width set to 10.
        worksheet.set_column('C:C', 30)  # Columns C width set to 30.
        worksheet.set_column('D:D', 10)  
        worksheet.set_column('E:E', 15)  
        worksheet.set_column('F:F', 15)  
        worksheet.set_column('G:G', 12)  
        worksheet.set_column('H:H', 12)  
        worksheet.set_column('I:I', 12)  
        worksheet.set_column('J:J', 12)  
        worksheet.set_column('K:K', 12)  
        worksheet.set_column('L:L', 35)  
        worksheet.set_column('M:M', 15)  
        worksheet.set_column('N:N', 15)  
        worksheet.set_column('O:O', 15)  
        worksheet.set_column('P:P', 15)  
        worksheet.set_column('Q:Q', 15)  
        worksheet.set_column('R:R', 15)  
        worksheet.set_column('S:S', 12)  
        worksheet.set_column('T:T', 12)  
        worksheet.set_column('U:U', 19)  
        worksheet.set_column('V:V', 16)  
        worksheet.set_column('W:W', 7)  
        worksheet.set_column('X:X', 15)  
        worksheet.set_column('Y:Y', 6)  
        worksheet.set_column('Z:Z', 10)  
        worksheet.set_column('AA:AA', 15)  
        worksheet.set_column('AB:AB', 18)  
        worksheet.set_column('AC:AC', 15)  
        worksheet.set_column('AD:AD', 15)  
        worksheet.set_column('AE:AE', 18)  
        worksheet.set_column('AF:AF', 18)  
        worksheet.set_column('AG:AG', 35)  
        worksheet.set_column('AH:AH', 25)  
        worksheet.set_column('AI:AI', 25)  
        worksheet.set_column('AJ:AJ', 25)  
        worksheet.set_column('AK:AK', 25)  

        # write column header
        worksheet.write("B2", "PT. XACTI INDONESIA", font14)
        worksheet.write("B3", "Active Employee List With Salary", font12)

        worksheet.write("B5", "IDNO", bold)
        worksheet.write("C5", "NAME", bold)
        worksheet.write("D5", "GENDER", bold)
        worksheet.write("E5", "BIRTH DATE", bold)
        worksheet.write("F5", "BIRTH PLACE", bold)
        worksheet.write("G5", "MARITAL STS", bold)
        worksheet.write("H5", "EDUCATION", bold)
        worksheet.write("I5", "DEPT CODE", bold)
        worksheet.write("J5", "SECT CODE", bold)
        worksheet.write("K5", "SUBSEC CODE", bold)
        worksheet.write("L5", "DEPT/SECTION NAMR", bold)
        worksheet.write("M5", "GRADE CODE", bold)
        worksheet.write("N5", "WORK GROUP", bold)
        worksheet.write("O5", "ADDRESS", bold)
        worksheet.write("P5", "EMPL-STS", bold)
        worksheet.write("Q5", "JOINT ENTRY", bold)
        worksheet.write("R5", "CONTRACT STS", bold)
        worksheet.write("S5", "START DATE", bold)
        worksheet.write("T5", "END DATE", bold)
        worksheet.write("U5", "TERMINATION DATE", bold)
        worksheet.write("V5", "POSITION", bold)
        worksheet.write("W5", "DIRECT", bold)
        worksheet.write("X5", "PHONE", bold)
        worksheet.write("Y5", "CLASS", bold)
        worksheet.write("Z5", "RELIGION", bold)
        worksheet.write("AA5", "SPMI MEMBER", bold)
        worksheet.write("AB5", "ID CARD NUMBER", bold)
        worksheet.write("AC5", "BPJS-TK ID", bold)
        worksheet.write("AD5", "BPJS-KES ID", bold)
        worksheet.write("AE5", "TAX-ID/NPWP", bold)
        worksheet.write("AF5", "BANK ACC NUMBER", bold)
        worksheet.write("AG5", "BANK ACC NAME", bold)
        worksheet.write("AH5", "DEPT. GROUP-1", bold)
        worksheet.write("AI5", "DEPT. GROUP-2", bold)
        worksheet.write("AJ5", "DEPT. GROUP-3", bold)
        worksheet.write("AK5", "DEPT. GROUP-4", bold)

        # write data to worksheet
        row = 5
        for line in self.detail_ids:
            worksheet.write(row, 1, line.IDNO)
            worksheet.write(row, 2, line.NAME)
            worksheet.write(row, 3, line.GENDER)
            worksheet.write(row, 4, line.DATBIR, date)
            worksheet.write(row, 5, line.PLACE)
            worksheet.write(row, 6, line.MARSTS)
            worksheet.write(row, 7, line.EDUC)
            worksheet.write(row, 8, line.DEPT)
            worksheet.write(row, 9, line.SECT)
            worksheet.write(row, 10, line.SBSEC)
            worksheet.write(row, 11, line.DESC)
            worksheet.write(row, 12, line.ALLCD)
            worksheet.write(row, 13, line.WRKGRP)
            worksheet.write(row, 14, line.ADDRESS)
            worksheet.write(row, 15, line.EMPSTS)
            worksheet.write(row, 16, line.DATENT, date)
            worksheet.write(row, 17, line.STSCNT)
            worksheet.write(row, 18, line.STRDAT, date)
            worksheet.write(row, 19, line.ENDDAT, date)
            worksheet.write(row, 20, line.TERDAT, date)
            worksheet.write(row, 21, line.POSIT)
            worksheet.write(row, 22, line.DIRECT)
            worksheet.write(row, 23, line.PHONE)
            worksheet.write(row, 24, line.CLASS)
            worksheet.write(row, 25, line.RELIGION)
            worksheet.write(row, 26, line.SPMI)
            worksheet.write(row, 27, line.KTPNO)
            worksheet.write(row, 28, line.BPJSTK_ID)
            worksheet.write(row, 29, line.BPJSKES_ID)
            worksheet.write(row, 30, line.NPWP)
            worksheet.write(row, 31, line.ACC_NUMBER)
            worksheet.write(row, 32, line.ACC_NAME)
            worksheet.write(row, 33, line.GROUP_1)
            worksheet.write(row, 34, line.GROUP_2)
            worksheet.write(row, 35, line.GROUP_3)
            worksheet.write(row, 36, line.GROUP_4)

            row += 1

        workbook.close()

        file_data.seek(0)
        self.export_file = base64.encodestring(file_data.getvalue())
        self.export_filename = 'Active Employee List-%s-%s-%s.xlsx' % (self.day, self.month, self.year)
    
class report_emp_active_01_detail(models.Model):
    _name = 'aag.report_emp_active_01_detail'
    _description = 'payroll emp_active_01 detail'

    header_id = fields.Many2one(comodel_name="aag.report_emp_active_01_header")

    IDNO            = fields.Integer("IDNO")
    NAME            = fields.Char("NAME")
    GENDER          = fields.Char("GENDER")
    DATBIR          = fields.Date("DATE OF BIRTH")
    PLACE           = fields.Char("PLACE OF BIRTH")
    MARSTS          = fields.Char("MARITAL STATUS")
    EDUC            = fields.Char("EDUCATION")
    DEPT            = fields.Integer("DEPT CODE")
    SECT            = fields.Integer("SECTION CODE")
    SBSEC           = fields.Integer("SUB-SECTION CODE")
    DESC            = fields.Char("DEPT/SECTION NAME")
    ALLCD           = fields.Char("GRADE CODE")
    WRKGRP          = fields.Char("WORK GROUP")
    ADDRESS         = fields.Char("ADDRESS")
    EMPSTS          = fields.Char("EMPL. STATUS")
    DATENT          = fields.Date("JOINT DATE")
    STSCNT          = fields.Char("CONTRACT STS")
    STRDAT          = fields.Date("DATE START")
    ENDDAT          = fields.Date("DATE END")
    TERDAT          = fields.Date("TERMINATION DATE")
    POSIT           = fields.Char("POSITION")
    DIRECT          = fields.Boolean("DIRECT")
    PHONE           = fields.Char("PHONE")
    CLASS           = fields.Char("CLASS")
    RELIGION        = fields.Char("RELIGION")
    SPMI            = fields.Boolean("SPMI")
    KTPNO           = fields.Char("KTPNO")
    BPJSTK_ID       = fields.Char("BPJSTK_ID")
    BPJSKES_ID      = fields.Char("BPJSKES_ID")
    NPWP            = fields.Char("NPWP")
    ACC_NUMBER      = fields.Char("ACC NUMBER")
    ACC_NAME        = fields.Char("ACC NAME")
    GROUP_1         = fields.Char("GROUP-1")
    GROUP_2         = fields.Char("GROUP-2")
    GROUP_3         = fields.Char("GROUP-3")
    GROUP_4         = fields.Char("GROUP-4")


