# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)
import xlsxwriter

import base64
from io import BytesIO
# from io import StringIO

class report_header(models.Model):
    _name = 'aag.report_header'
    _description = 'payroll header'

    name = fields.Char("Name")
    month = fields.Integer("Month")
    year = fields.Integer("Year")

    export_file = fields.Binary("Export File")
    export_filename = fields.Char(string="Export File Name",  )

    detail_ids = fields.One2many(comodel_name="aag.report_detail", inverse_name="header_id")

    def action_generate(self):
        cr = self.env.cr

        sql = "delete from aag_report_detail where header_id=%s"
        cr.execute(sql, (self.id,))

        sql = """
            INSERT INTO aag_report_detail (
                header_id,
                "IDNO",
                "NAME",
                "EMPSTS",
                "DIRECT",
                "DEPT",
                "SECT",
                "SBSEC",
                "DESC",
                "BASIC",
                "I_BASIC",
                "I_THR",
                "I_BONUS",
                "I_TPK",
                "I_OCCUP",
                "I_FAMILY",
                "I_FUNCTIONAL",
                "I_MEDICAL",
                "I_TRANSPORT",
                "I_PERFORM",
                "I_MEAL",
                "I_SHIFT",
                "I_LEAVE",
                "I_OTHER",
                "I_OVERTIME",
                "I_RSGALLW",
                "I_DONATION",
                "I_PRVROUND",
                "I_PPH_DTP",
                "D_LOAN",
                "D_SPMI",
                "D_KOPERASI",
                "D_BASIC",
                "D_TRANSPORT",
                "D_OTHER",
                "D_MEDICAL",
                "D_JHTEMP",
                "D_BPJSKES_EMP",
                "D_PENEMP",
                "D_CURRND",
                "C_PPH21",
                "C_JHTCOM",
                "C_ACCCOM",
                "C_DTHCOM",
                "C_BPJSKES_COM",
                "C_PENCOM",
                "NET",
                "MED_BALANCE",
                "LEAVE_BALANCE",
                "GROUP_1",
                "GROUP_2",
                "GROUP_3",
                "GROUP_4",
                "x_male",
                "x_female",
                "ALLCD",
                "POSIT"

            ) 
            SELECT 
                %s,
                emp.x_idno, emp.name, emp.x_empsts as EMPSTS, emp.x_direct as DIRECT,
                emp.x_dept as DEPT, emp.x_sect as SECT, emp.x_sbsec as SBSEC, dept.x_desc as DESC,
                ps.basic as BASIC, ps.i_basic as I_BASIC,
                ps.i_thr as I_THR, ps.i_bonus as I_BONUS,
                ps.i_tpk as I_TPK, ps.i_occup as I_OCCUP,
                ps.i_family as I_FAMILY, ps.i_functional as I_FUNCTIONAL,
                ps.i_medical as I_MEDICAL, ps.i_transport as I_TRANSPORT,
                ps.i_perform as I_PERFORM, ps.i_meal as I_MEAL,
                ps.i_shift as I_SHIFT, ps.i_leave as I_LEAVE,
                ps.i_other as I_OTHER, ps.i_overtime as I_OVERTIME,
                0 as I_IRSGALLW, 0 as I_DONATION, 0 as I_PRVROUND,
                ps.i_pphdtp as I_PPHDTP, ps.d_loan as D_LOAN,
                ps.d_spmi as D_SPMI, ps.d_koperasi as D_KOPERASI,
                ps.d_basic as D_BASIC, ps.d_transport as D_TRANSPORT,
                ps.d_other as D_OTHER, ps.d_medical as D_MEDICAL,
                ps.d_jhtemp as D_JHTEMP, ps.d_bpjs_emp as D_BPJSKES_EMP,
                ps.d_penemp as D_PENEMP, 0 as D_CURRND,
                ps.tunj_pph as C_PPH21, 
                ps.i_jhtcom as C_JHTCOM, ps.i_acccom as C_ACCCOM, ps.i_dthcom as C_DTHCOM, ps.i_bpjs_com as C_BPJSKES_COM, ps.i_pencom as C_PENCOM,   
                ps.net as NET, 
                ps.curr_med_bal as MED_BALANCCE, ps.curr_leave_bal as LEAVE_BALANCCE,
                grp.x_group1 as GROUP_1,
                grp.x_group2 as GROUP_2,
                grp.x_group3 as GROUP_3,
                grp.x_group4 as GROUP_4,  
                case 
                    when emp.gender='male' then 1
                    else 0
                end as x_male,
                case 
                    when emp.gender='female' then 1
                    else 0
                end as x_female,
                case 
                    when emp.x_allcd isnull then '  '
                    else emp.x_allcd
                end as ALLCD,
                job.name as POSIT
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
            join 
                hr_job job on emp.job_id = job.id                
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
        worksheet.set_column('D:D', 6)  
        worksheet.set_column('E:E', 6)  
        worksheet.set_column('F:F', 6)  
        worksheet.set_column('G:G', 35)  
        worksheet.set_column('H:H', 12)  
        worksheet.set_column('I:I', 9)  
        worksheet.set_column('J:J', 9)  
        worksheet.set_column('K:K', 9)  
        worksheet.set_column('L:L', 9)  
        worksheet.set_column('M:M', 12)  
        worksheet.set_column('N:N', 12)  
        worksheet.set_column('O:O', 14)  
        worksheet.set_column('P:P', 12)  
        worksheet.set_column('Q:Q', 14)  
        worksheet.set_column('R:R', 12)  
        worksheet.set_column('S:S', 8)  
        worksheet.set_column('T:T', 8)  
        worksheet.set_column('U:U', 8)  
        worksheet.set_column('V:V', 8)  
        worksheet.set_column('W:W', 12)  
        worksheet.set_column('X:X', 12)  
        worksheet.set_column('Y:Y', 12)  
        worksheet.set_column('Z:Z', 12)  
        worksheet.set_column('AA:AA', 12)  
        worksheet.set_column('AB:AB', 10)  
        worksheet.set_column('AC:AC', 10)  
        worksheet.set_column('AD:AD', 12)  
        worksheet.set_column('AE:AE', 12)  
        worksheet.set_column('AF:AF', 14)  
        worksheet.set_column('AG:AG', 12)  
        worksheet.set_column('AH:AH', 12)  
        worksheet.set_column('AI:AI', 12)  
        worksheet.set_column('AJ:AJ', 16)  
        worksheet.set_column('AK:AK', 12)  
        worksheet.set_column('AL:AL', 12)  
        worksheet.set_column('AM:AM', 12)  
        worksheet.set_column('AN:AN', 12)  
        worksheet.set_column('AO:AO', 12)  
        worksheet.set_column('AP:AP', 12)  
        worksheet.set_column('AQ:AQ', 16)  
        worksheet.set_column('AR:AR', 12)  
        worksheet.set_column('AS:AS', 12)  
        worksheet.set_column('AT:AT', 8)  
        worksheet.set_column('AU:AU', 7)  
        worksheet.set_column('AV:AV', 15)  
        worksheet.set_column('AW:AW', 15)  
        worksheet.set_column('AX:AX', 25)  
        worksheet.set_column('AY:AY', 18)  
        worksheet.set_column('AZ:AZ', 25)  
        worksheet.set_column('BA:BA', 10)  
        worksheet.set_column('BB:BB', 10)  
        worksheet.set_column('BC:BC', 10)  
        worksheet.set_column('BD:BD', 10)  
        worksheet.set_column('BE:BE', 20)  

        # write header
        worksheet.write("B2", "PT. XACTI INDONESIA", font14)
        worksheet.write("B3", "Monthly Salary Detail Report", font12)

        worksheet.write("B5", "IDNO", bold)
        worksheet.write("C5", "NAME", bold)
        worksheet.write("D5", "DEPT", bold)
        worksheet.write("E5", "SECT", bold)
        worksheet.write("F5", "SBSEC", bold)
        worksheet.write("G5", "DESC", bold)
        worksheet.write("H5", "BASIC", bold)
        worksheet.write("I5", "I-BASIC", bold)
        worksheet.write("J5", "I-THR", bold)
        worksheet.write("K5", "I-BONUS", bold)
        worksheet.write("L5", "I-TPK", bold)
        worksheet.write("M5", "I-OCCUP", bold)
        worksheet.write("N5", "I-FAMILY", bold)
        worksheet.write("O5", "I-FUNCTIONAL", bold)
        worksheet.write("P5", "I-MEDICAL", bold)
        worksheet.write("Q5", "I-TRANSPORT", bold)
        worksheet.write("R5", "I-PERFORM", bold)
        worksheet.write("S5", "I-MEAL", bold)
        worksheet.write("T5", "I-SHIFT", bold)
        worksheet.write("U5", "I-LEAVE", bold)
        worksheet.write("V5", "I-OTHER", bold)
        worksheet.write("W5", "I-OVERTIME", bold)
        worksheet.write("X5", "I-RSGALLW", bold)
        worksheet.write("Y5", "I-DONATION", bold)
        worksheet.write("Z5", "I-PRVROUND", bold)
        worksheet.write("AA5", "I-PPH_DTP", bold)
        worksheet.write("AB5", "D-LOAN", bold)
        worksheet.write("AC5", "D-SPMI", bold)
        worksheet.write("AD5", "D-KOPERASI", bold)
        worksheet.write("AE5", "D-BASIC", bold)
        worksheet.write("AF5", "D-TRANSPORT", bold)
        worksheet.write("AG5", "D-OTHER", bold) 
        worksheet.write("AH5", "D-MEDICAL", bold)
        worksheet.write("AI5", "D-JHTEMP", bold)
        worksheet.write("AJ5", "D-BPJSKES_EMP", bold)
        worksheet.write("AK5", "D-PENEMP", bold)
        worksheet.write("AL5", "D-CURRND", bold)
        worksheet.write("AM5", "C-PPH21", bold)
        worksheet.write("AN5", "C-JHTCOM", bold)
        worksheet.write("AO5", "C-ACCCOM", bold)
        worksheet.write("AP5", "C-DTHCOM", bold)
        worksheet.write("AQ5", "C-BPJSKES_COM", bold)
        worksheet.write("AR5", "C-PENCOM", bold)
        worksheet.write("AS5", "NET", bold)
        worksheet.write("AT5", "EMPSTS", bold)
        worksheet.write("AU5", "DIRECT", bold)
        worksheet.write("AV5", "MED. BALANCE", bold)
        worksheet.write("AW5", "LEAVE BALANCE", bold)
        worksheet.write("AX5", "DEPT. GROUP-1", bold)
        worksheet.write("AY5", "DEPT. GROUP-2", bold)
        worksheet.write("AZ5", "DEPT. GROUP-3", bold)
        worksheet.write("BA5", "DEPT. GROUP-4", bold)
        worksheet.write("BB5", "MALE", bold)
        worksheet.write("BC5", "FEMALE", bold)
        worksheet.write("BD5", "GRADE", bold)
        worksheet.write("BE5", "POSITION", bold)

        # write data 
        row = 5
        for line in self.detail_ids:
            worksheet.write(row, 1, line.IDNO)
            worksheet.write(row, 2, line.NAME)
            worksheet.write(row, 3, line.DEPT)
            worksheet.write(row, 4, line.SECT)
            worksheet.write(row, 5, line.SBSEC)
            worksheet.write(row, 6, line.DESC)
            worksheet.write(row, 7, line.BASIC, numeric)
            worksheet.write(row, 8, line.I_BASIC, numeric)
            worksheet.write(row, 9, line.I_THR, numeric)
            worksheet.write(row, 10, line.I_BONUS, numeric)
            worksheet.write(row, 11, line.I_TPK, numeric)
            worksheet.write(row, 12, line.I_OCCUP, numeric)
            worksheet.write(row, 13, line.I_FAMILY, numeric)
            worksheet.write(row, 14, line.I_FUNCTIONAL, numeric)
            worksheet.write(row, 15, line.I_MEDICAL, numeric) 
            worksheet.write(row, 16, line.I_TRANSPORT, numeric)
            worksheet.write(row, 17, line.I_PERFORM, numeric)
            worksheet.write(row, 18, line.I_MEAL, numeric)
            worksheet.write(row, 19, line.I_SHIFT, numeric)
            worksheet.write(row, 20, line.I_LEAVE, numeric)
            worksheet.write(row, 21, line.I_OTHER, numeric)
            worksheet.write(row, 22, line.I_OVERTIME, numeric)
            worksheet.write(row, 23, line.I_RSGALLW, numeric)
            worksheet.write(row, 24, line.I_DONATION, numeric)
            worksheet.write(row, 25, line.I_PRVROUND, numeric)
            worksheet.write(row, 26, line.I_PPH_DTP, numeric)
            worksheet.write(row, 27, line.D_LOAN, numeric)
            worksheet.write(row, 28, line.D_SPMI, numeric)
            worksheet.write(row, 29, line.D_KOPERASI, numeric)
            worksheet.write(row, 30, line.D_BASIC, numeric)
            worksheet.write(row, 31, line.D_TRANSPORT, numeric)
            worksheet.write(row, 32, line.D_OTHER, numeric)
            worksheet.write(row, 33, line.D_MEDICAL, numeric)
            worksheet.write(row, 34, line.D_JHTEMP, numeric)
            worksheet.write(row, 35, line.D_BPJSKES_EMP, numeric)
            worksheet.write(row, 36, line.D_PENEMP, numeric)
            worksheet.write(row, 37, line.D_CURRND, numeric)
            worksheet.write(row, 38, line.C_PPH21, numeric)
            worksheet.write(row, 39, line.C_JHTCOM, numeric)
            worksheet.write(row, 40, line.C_ACCCOM, numeric)
            worksheet.write(row, 41, line.C_DTHCOM, numeric)
            worksheet.write(row, 42, line.C_BPJSKES_COM, numeric)
            worksheet.write(row, 43, line.C_PENCOM, numeric)
            worksheet.write(row, 44, line.NET, numeric)
            worksheet.write(row, 45, line.EMPSTS)
            worksheet.write(row, 46, line.DIRECT)
            worksheet.write(row, 47, line.MED_BALANCE, numeric)
            worksheet.write(row, 48, line.LEAVE_BALANCE, numeric2)
            worksheet.write(row, 49, line.GROUP_1)
            worksheet.write(row, 50, line.GROUP_2)
            worksheet.write(row, 51, line.GROUP_3)
            worksheet.write(row, 52, line.GROUP_4)
            worksheet.write(row, 53, line.x_male)
            worksheet.write(row, 54, line.x_female)
            worksheet.write(row, 55, line.ALLCD)
            worksheet.write(row, 56, line.POSIT)
            row += 1

        workbook.close()

        file_data.seek(0)
        self.export_file = base64.encodestring(file_data.getvalue())
        self.export_filename = 'report_payroll-%s-%s.xlsx' % (self.month, self.year)

        #_logger.info("--- action_export")


class report_detail(models.Model):
    _name = 'aag.report_detail'
    _description = 'payroll detail'

    header_id = fields.Many2one(comodel_name="aag.report_header")

    IDNO            = fields.Integer("IDNO")
    NAME            = fields.Char("NAME")
    EMPSTS          = fields.Char("EMPSTS")
    DIRECT          = fields.Char("DIRECT")
    DEPT            = fields.Integer("DEPT")
    SECT            = fields.Integer("SECT")
    SBSEC           = fields.Integer("SBSEC")
    DESC            = fields.Char("DEPT/SECTION")
    BASIC           = fields.Integer("BASIC")
    I_BASIC         = fields.Integer("I_BASIC")
    I_THR           = fields.Integer("I_THR")
    I_BONUS         = fields.Integer("I_BONUS")
    I_TPK           = fields.Integer("I_TPK")
    I_OCCUP         = fields.Integer("I_OCCUP")
    I_FAMILY        = fields.Integer("I_FAMILY")
    I_FUNCTIONAL    = fields.Integer("I_FUNCTIONAL")
    I_MEDICAL       = fields.Integer("I_MEDICAL")
    I_TRANSPORT     = fields.Integer("I_TRANSPORT")
    I_PERFORM       = fields.Integer("I_PERFORMANCE")
    I_MEAL          = fields.Integer("I_MEAL")
    I_SHIFT         = fields.Integer("I_SHIFT")
    I_LEAVE         = fields.Integer("I_LEAVE")
    I_OTHER         = fields.Integer("I_OTHER")
    I_OVERTIME      = fields.Integer("I_OVERTIME")
    I_RSGALLW       = fields.Integer("I_RESIGN-ALW.")
    I_DONATION      = fields.Integer("I_DONATION")
    I_PRVROUND      = fields.Integer("I_PRVROUND")
    I_PPH_DTP       = fields.Integer("I_PPH_DTP")
    D_LOAN          = fields.Integer("D_LOAN")
    D_SPMI          = fields.Integer("D_SPMI")
    D_KOPERASI      = fields.Integer("D_KOPERASI")
    D_BASIC         = fields.Integer("D_BASIC")
    D_TRANSPORT     = fields.Integer("D_TRANSPORT")
    D_OTHER         = fields.Integer("D_OTHER")
    D_MEDICAL       = fields.Integer("D_MEDICAL")
    D_JHTEMP        = fields.Integer("D_JHTEMP")
    D_BPJSKES_EMP   = fields.Integer("D_BPJSKES_EMP")
    D_PENEMP        = fields.Integer("D_PENEMP")
    D_CURRND        = fields.Integer("D_CURRND")
    C_PPH21         = fields.Integer("C_PPH21")
    C_JHTCOM        = fields.Integer("C_JHT 3.7%")
    C_ACCCOM        = fields.Integer("C_JKK 0.89%")
    C_DTHCOM        = fields.Integer("C_JKM 0.3%")
    C_BPJSKES_COM   = fields.Integer("C_BPJS-KES 4%")
    C_PENCOM        = fields.Integer("C_PENSION 2%")
    NET             = fields.Integer("NET")
    MED_BALANCE     = fields.Float("MED BALANCE")
    LEAVE_BALANCE   = fields.Float("LEAVE BALANCE")
    GROUP_1         = fields.Char("GROUP-1")
    GROUP_2         = fields.Char("GROUP-2")
    GROUP_3         = fields.Char("GROUP-3")
    GROUP_4         = fields.Char("GROUP-4")
    x_male          = fields.Integer("Male")
    x_female        = fields.Integer("Female")
    ALLCD           = fields.Char("Grade")
    POSIT           = fields.Char("Position")


