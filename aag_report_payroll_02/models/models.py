# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)
import xlsxwriter

import base64
from io import BytesIO
# from io import StringIO

class report_01_header(models.Model):
    _name = 'aag.report_01_header'
    _description = 'payroll header'

    name = fields.Char("Name")
    month = fields.Integer("Month")
    year = fields.Integer("Year")

    export_file = fields.Binary("Export File")
    export_filename = fields.Char(string="Export File Name",  )

    detail_ids = fields.One2many(comodel_name="aag.report_01_detail", inverse_name="header_id")

    def action_generate(self):
        cr = self.env.cr

        sql = "delete from aag_report_01_detail where header_id=%s"
        cr.execute(sql, (self.id,))

        sql = """
            INSERT INTO aag_report_01_detail (
                header_id,
                "x_idno",
                "x_name",
                "x_empsts",
                "x_gender",
                "x_emploc",
                "x_dept",
                "x_sect",
                "x_sbsec",
                "x_desc",
                "basic",
                "i_basic",
                "x_group_1",
                "x_group_2",
                "x_group_3",
                "x_group_4"
            ) 
            SELECT 
                %s,
                emp.x_idno, emp.name as x_name, emp.x_empsts,
                (case when emp.gender='male' then 'Male' else 'Female' end) as x_gender, 
                (case when emp.x_direct=True then 'Direct' else 'Indirect' end) as x_emploc, 
                emp.x_dept, emp.x_sect, emp.x_sbsec, dept.x_desc,
                case when ps.basic isnull then 0 else ps.basic end,
                case when ps.i_basic isnull then 0 else ps.i_basic end,
                grp.x_group1 as x_group_1,
                grp.x_group2 as x_group_2,
                grp.x_group3 as x_group_3,
                grp.x_group4 as x_group_4  
            from 
                hr_payslip ps 
            join 
                hr_employee emp on ps.employee_id = emp.id
            join 
                aag_dept_master_aag_dept_master dept on dept.x_dept = emp.x_dept
                and dept.x_sect = emp.x_sect
                and dept.x_sbsec = emp.x_sbsec
            join 
                aag_dept_group_aag_dept_group grp on emp.x_dept = grp.x_dept
            where
                date_part('month', ps.date_to) = %s
                and date_part('year', ps.date_to) = %s
        """
        cr.execute(sql, (self.id, self.month, self.year))

        # _logger.info("--- done action_generate")


    def action_export(self):
        file_data = BytesIO()
        workbook = xlsxwriter.Workbook(file_data)
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        font12 = workbook.add_format({'bold': True, 'font_size': 12})
        font14 = workbook.add_format({'bold': True, 'font_size': 14})
        numeric = workbook.add_format({'num_format': '#,##0'})
        numeric2 = workbook.add_format({'num_format': '#,##0.00'})

        # SET COLUMN WIDTH
        worksheet.set_column('B:B', 8)  # Column  B width set to 10.
        worksheet.set_column('C:C', 30)  # Columns C width set to 30.
        worksheet.set_column('D:D', 10)  
        worksheet.set_column('E:E', 10)  
        worksheet.set_column('F:F', 8)  
        worksheet.set_column('G:G', 6)  
        worksheet.set_column('H:H', 6)  
        worksheet.set_column('I:I', 6)  
        worksheet.set_column('J:J', 30)  
        worksheet.set_column('K:K', 12)  
        worksheet.set_column('L:L', 12)  

        worksheet.set_column('AX:AX', 25)  
        worksheet.set_column('AY:AY', 18)  
        worksheet.set_column('AZ:AZ', 25)  
        worksheet.set_column('BA:BA', 15)  

        # write header
        worksheet.write("B2", "PT. XACTI INDONESIA", font14)
        worksheet.write("B3", "Monthly Salary Detail Report", font12)

        worksheet.write("B5", "IDNO", bold)
        worksheet.write("C5", "NAME", bold)
        worksheet.write("D5", "EMP-STS", bold)
        worksheet.write("E5", "GENDER", bold)
        worksheet.write("F5", "LOC", bold)
        worksheet.write("G5", "DEPT", bold)
        worksheet.write("H5", "SECT", bold)
        worksheet.write("I5", "SBSEC", bold)
        worksheet.write("J5", "DESC", bold)
        worksheet.write("K5", "BASIC", bold)
        worksheet.write("L5", "I-BASIC", bold)
        worksheet.write("M5", "I-THR", bold)
        worksheet.write("N5", "I-BONUS", bold)
        worksheet.write("O5", "I-TPK", bold)
        worksheet.write("P5", "I-OCCUP", bold)
        worksheet.write("Q5", "I-FAMILY", bold)
        worksheet.write("R5", "I-FUNCTIONAL", bold)
        worksheet.write("S5", "I-MEDICAL", bold)
        worksheet.write("T5", "I-TRANSPORT", bold)
        worksheet.write("U5", "I-PERFORM", bold)
        worksheet.write("V5", "I-MEAL", bold)
        worksheet.write("W5", "I-SHIFT", bold)
        worksheet.write("X5", "I-LEAVE", bold)
        worksheet.write("Y5", "I-OTHER", bold)
        worksheet.write("Z5", "I-OVERTIME", bold)
        worksheet.write("AA5", "I-RSGALLW", bold)
        worksheet.write("AB5", "I-DONATION", bold)
        worksheet.write("AC5", "I-PRVROUND", bold)
        worksheet.write("AD5", "I-PPH_DTP", bold)
        worksheet.write("AE5", "D-LOAN", bold)
        worksheet.write("AF5", "D-SPMI", bold)
        worksheet.write("AG5", "D-KOPERASI", bold)
        worksheet.write("AH5", "D-BASIC", bold)
        worksheet.write("AI5", "D-TRANSPORT", bold)
        worksheet.write("AJ5", "D-OTHER", bold) 
        worksheet.write("AK5", "D-MEDICAL", bold)
        worksheet.write("AL5", "D-JHTEMP", bold)
        worksheet.write("AM5", "D-BPJSKES_EMP", bold)
        worksheet.write("AN5", "D-PENEMP", bold)
        worksheet.write("AO5", "D-CURRND", bold)
        worksheet.write("AP5", "C-PPH21", bold)
        worksheet.write("AQ5", "C-JHTCOM", bold)
        worksheet.write("AR5", "C-ACCCOM", bold)
        worksheet.write("AS5", "C-DTHCOM", bold)
        worksheet.write("AT5", "C-BPJSKES_COM", bold)
        worksheet.write("AU5", "C-PENCOM", bold)
        worksheet.write("AV5", "NET", bold)
        worksheet.write("AW5", "MED. BALANCE", bold)
        worksheet.write("AX5", "LEAVE BALANCE", bold)
        worksheet.write("AY5", "DEPT. GROUP-1", bold)
        worksheet.write("AZ5", "DEPT. GROUP-2", bold)
        worksheet.write("BA5", "DEPT. GROUP-3", bold)
        worksheet.write("BB5", "DEPT. GROUP-4", bold)

        # write data 
        row = 5
        for line in self.detail_ids:
            worksheet.write(row, 1, line.x_idno)
            worksheet.write(row, 2, line.x_name)
            worksheet.write(row, 3, line.x_empsts)
            worksheet.write(row, 4, line.x_gender)
            worksheet.write(row, 5, line.x_emploc)
            worksheet.write(row, 6, line.x_dept)
            worksheet.write(row, 7, line.x_sect)
            worksheet.write(row, 8, line.x_sbsec)
            worksheet.write(row, 9, line.x_desc)
            worksheet.write(row, 10, line.basic, numeric)
            worksheet.write(row, 11, line.i_basic, numeric)
            worksheet.write(row, 12, line.i_thr, numeric)
            worksheet.write(row, 13, line.i_bonus, numeric)
            worksheet.write(row, 14, line.i_tpk, numeric)
            worksheet.write(row, 15, line.i_occup, numeric)
            worksheet.write(row, 16, line.i_family, numeric)
            worksheet.write(row, 17, line.i_functional, numeric)
            worksheet.write(row, 18, line.i_medical, numeric) 
            worksheet.write(row, 19, line.i_transport, numeric)
            worksheet.write(row, 20, line.i_perform, numeric)
            worksheet.write(row, 21, line.i_meal, numeric)
            worksheet.write(row, 22, line.i_shift, numeric)
            worksheet.write(row, 23, line.i_leave, numeric)
            worksheet.write(row, 24, line.i_other, numeric)
            worksheet.write(row, 25, line.i_overtime, numeric)
            worksheet.write(row, 26, line.i_rsgallw, numeric)
            worksheet.write(row, 27, line.i_donation, numeric)
            worksheet.write(row, 28, line.i_prvroud, numeric)
            worksheet.write(row, 29, line.i_pph_dtp, numeric)
            worksheet.write(row, 30, line.d_loan, numeric)
            worksheet.write(row, 31, line.d_spmi, numeric)
            worksheet.write(row, 32, line.d_koperasi, numeric)
            worksheet.write(row, 33, line.d_basic, numeric)
            worksheet.write(row, 34, line.d_transport, numeric)
            worksheet.write(row, 35, line.d_other, numeric)
            worksheet.write(row, 36, line.d_medical, numeric)
            worksheet.write(row, 37, line.d_jhtemp, numeric)
            worksheet.write(row, 38, line.d_bpjskes_emp, numeric)
            worksheet.write(row, 39, line.d_penemp, numeric)
            worksheet.write(row, 40, line.d_currnd, numeric)
            worksheet.write(row, 41, line.c_pph21, numeric)
            worksheet.write(row, 42, line.c_jhtcom, numeric)
            worksheet.write(row, 43, line.c_acccom, numeric)
            worksheet.write(row, 44, line.c_dthcom, numeric)
            worksheet.write(row, 45, line.c_bpjskes_com, numeric)
            worksheet.write(row, 46, line.c_pencom, numeric)
            worksheet.write(row, 47, line.net, numeric)
            worksheet.write(row, 48, line.med_balance, numeric)
            worksheet.write(row, 49, line.leave_balance, numeric2)
            worksheet.write(row, 50, line.x_group_1)
            worksheet.write(row, 51, line.x_group_2)
            worksheet.write(row, 52, line.x_group_3)
            worksheet.write(row, 53, line.x_group_4)

            row += 1

        workbook.close()

        file_data.seek(0)
        self.export_file = base64.encodestring(file_data.getvalue())
        self.export_filename = 'report_01_payroll-%s-%s.xlsx' % (self.month, self.year)

        #_logger.info("--- action_export")


class report_01_detail(models.Model):
    _name = 'aag.report_01_detail'
    _description = 'payroll detail'

    header_id = fields.Many2one(comodel_name="aag.report_01_header")

    x_idno          = fields.Integer("IDNO")
    x_name          = fields.Char("NAME")
    x_empsts        = fields.Char("EMPL. STS")
    x_gender        = fields.Char("GENDER")
    x_emploc        = fields.Char("EMPL. LOC")
    x_dept          = fields.Integer("DEPT")
    x_sect          = fields.Integer("SECT")
    x_sbsec         = fields.Integer("SBSEC")
    x_desc          = fields.Char("DEPT/SECTION")
    basic           = fields.Integer("Basic Salary")
    i_basic         = fields.Integer("I-Basic")
    x_group_1       = fields.Char("GROUP-1")
    x_group_2       = fields.Char("GROUP-2")
    x_group_3       = fields.Char("GROUP-3")
    x_group_4       = fields.Char("GROUP-4")


