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
                "C_BPJSKES_COM",
                "C_PENCOM",
                "NET"
            ) 
            SELECT 
                %s,
                emp.x_idno, 

                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='BASIC'),0) as BASIC,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='I_BASIC'),0) as I_BASIC,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='I_THR'),0) as I_THR,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='I_BONUS'),0) as I_BONUS,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='I_TPK'),0) as I_TPK,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='I_OCCUP'),0) as I_OCCUP,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='I_FAMILY'),0) as I_FAMILY,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='I_FUNCTIONAL'),0) as I_FUNCTIONAL,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='I_MEDICAL'),0) as I_MEDICAL,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='I_TRANSPORT'),0) as I_TRANSPORT,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='I_PERFORM'),0) as I_PERFORM,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='I_MEAL'),0) as I_MEAL,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='I_SHIFT'),0) as I_SHIFT,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='I_LEAVE'),0) as I_LEAVE,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='I_OTHER'),0) as I_OTHER,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='I_OVERTIME'),0) as I_OVERTIME,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='I_LEAVE'),0) as I_IRSGALLW,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='I_LEAVE'),0) as I_DONATION,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='I_LEAVE'),0) as I_PRVROUND,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='I_LEAVE'),0) as D_LOAN,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='D_SPMI'),0) as D_SPMI,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='D_KOPERASI'),0) as D_KOPERASI,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='D_BASIC'),0) as D_BASIC,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='D_TRANSPORT'),0) as D_TRANSPORT,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='D_OTHER'),0) as D_OTHER,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='D_MEDICAL'),0) as D_MEDICAL,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='D_JHTEMP'),0) as D_JHTEMP,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='D_BPJSKES_EMP'),0) as D_BPJSKES_EMP,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='D_PENEMP'),0) as D_PENEMP,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='I_LEAVE'),0) as D_CURRND,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='D_PPH21'),0) as C_PPH21,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='D_JHTCOM'),0) as C_JHTCOM,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='D_BPJSKES_COM'),0) as C_BPJSKES_COM,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='D_PENCOM'),0) as C_PENCOM,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='NET'),0) as NET

            from 
                hr_payslip ps 
            join 
                hr_employee emp on ps.employee_id = emp.id
            where
                date_part('month', ps.date_to) = %s
                and date_part('year', ps.date_to) = %s
        """
        cr.execute(sql, (self.id, self.month, self.year))

        _logger.info("--- done action_generate")



    def action_export(self):
        file_data = BytesIO()
        workbook = xlsxwriter.Workbook(file_data)
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        numeric = workbook.add_format({'num_format': '#,##0'})

        # write header
        worksheet.write("A1", "IDNO", bold)
        worksheet.write("B1", "BASIC", bold)
        worksheet.write("C1", "I_BASIC", bold)
        worksheet.write("D1", "I_THR", bold)
        worksheet.write("E1", "I_BONUS", bold)
        worksheet.write("F1", "I_TPK", bold)
        worksheet.write("G1", "I_OCCUP", bold)
        worksheet.write("H1", "I_FAMILY", bold)
        worksheet.write("I1", "I_FUNCTIONAL", bold)
        worksheet.write("J1", "I_MEDICAL", bold)
        worksheet.write("K1", "I_TRANSPORT", bold)
        worksheet.write("L1", "I_PERFORM", bold)
        worksheet.write("M1", "I_MEAL", bold)
        worksheet.write("N1", "I_SHIFT", bold)
        worksheet.write("O1", "I_LEAVE", bold)
        worksheet.write("P1", "I_OTHER", bold)
        worksheet.write("Q1", "I_OVERTIME", bold)
        worksheet.write("R1", "I_RSGALLW", bold)
        worksheet.write("S1", "I_DONATION", bold)
        worksheet.write("T1", "I_PRVROUND", bold)
        worksheet.write("U1", "D_LOAN", bold)
        worksheet.write("V1", "D_SPMI", bold)
        worksheet.write("W1", "D_KOPERASI", bold)
        worksheet.write("X1", "D_BASIC", bold)
        worksheet.write("Y1", "D_TRANSPORT", bold)
        worksheet.write("Z1", "D_OTHER", bold)
        worksheet.write("AA1", "D_MEDICAL", bold)
        worksheet.write("AB1", "D_JHTEMP", bold)
        worksheet.write("AC1", "D_BPJSKES_EMP", bold)
        worksheet.write("AD1", "D_PENEMP", bold)
        worksheet.write("AE1", "D_CURRND", bold)
        worksheet.write("AF1", "C_PPH21", bold)
        worksheet.write("AG1", "C_JHTCOM", bold)
        worksheet.write("AH1", "C_BPJSKES_COM", bold)
        worksheet.write("AI1", "C_PENCOM", bold)
        worksheet.write("AJ1", "NET", bold)

        # write data 
        row = 1
        for line in self.detail_ids:
            worksheet.write(row, 0, line.IDNO)
            worksheet.write(row, 1, line.BASIC, numeric)
            worksheet.write(row, 2, line.I_BASIC, numeric)
            worksheet.write(row, 3, line.I_THR, numeric)
            worksheet.write(row, 4, line.I_BONUS, numeric)
            worksheet.write(row, 5, line.I_TPK, numeric)
            worksheet.write(row, 6, line.I_OCCUP, numeric)
            worksheet.write(row, 7, line.I_FAMILY, numeric)
            worksheet.write(row, 8, line.I_FUNCTIONAL, numeric)
            worksheet.write(row, 9, line.I_MEDICAL, numeric)
            worksheet.write(row, 10, line.I_TRANSPORT, numeric)
            worksheet.write(row, 11, line.I_PERFORM, numeric)
            worksheet.write(row, 12, line.I_MEAL, numeric)
            worksheet.write(row, 13, line.I_SHIFT, numeric)
            worksheet.write(row, 14, line.I_LEAVE, numeric)
            worksheet.write(row, 15, line.I_OTHER, numeric)
            worksheet.write(row, 16, line.I_OVERTIME, numeric)
            worksheet.write(row, 17, line.I_RSGALLW, numeric)
            worksheet.write(row, 18, line.I_DONATION, numeric)
            worksheet.write(row, 19, line.I_PRVROUND, numeric)
            worksheet.write(row, 20, line.D_LOAN, numeric)
            worksheet.write(row, 21, line.D_SPMI, numeric)
            worksheet.write(row, 22, line.D_KOPERASI, numeric)
            worksheet.write(row, 23, line.D_BASIC, numeric)
            worksheet.write(row, 24, line.D_TRANSPORT, numeric)
            worksheet.write(row, 25, line.D_OTHER, numeric)
            worksheet.write(row, 26, line.D_MEDICAL, numeric)
            worksheet.write(row, 27, line.D_JHTEMP, numeric)
            worksheet.write(row, 28, line.D_BPJSKES_EMP, numeric)
            worksheet.write(row, 29, line.D_PENEMP, numeric)
            worksheet.write(row, 30, line.D_CURRND, numeric)
            worksheet.write(row, 31, line.C_PPH21, numeric)
            worksheet.write(row, 32, line.C_JHTCOM, numeric)
            worksheet.write(row, 33, line.C_BPJSKES_COM, numeric)
            worksheet.write(row, 34, line.C_PENCOM, numeric)

            worksheet.write(row, 35, line.NET, numeric)
            row += 1

        workbook.close()

        file_data.seek(0)
        self.export_file = base64.encodestring(file_data.getvalue())
        self.export_filename = 'report_payroll-%s-%s.xlsx' % (self.month, self.year)




        _logger.info("--- action_export")


class report_detail(models.Model):
    _name = 'aag.report_detail'
    _description = 'payroll detail'

    header_id = fields.Many2one(comodel_name="aag.report_header")

    IDNO            = fields.Integer("IDNO")
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
    I_PERFORM       = fields.Integer("I_PERFORM")
    I_MEAL          = fields.Integer("I_MEAL")
    I_SHIFT         = fields.Integer("I_SHIFT")
    I_LEAVE         = fields.Integer("I_LEAVE")
    I_OTHER         = fields.Integer("I_OTHER")
    I_OVERTIME      = fields.Integer("I_OVERTIME")
    I_RSGALLW       = fields.Integer("I_RSGALLW")
    I_DONATION      = fields.Integer("I_DONATION")
    I_PRVROUND      = fields.Integer("I_PRVROUND")
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
    C_JHTCOM        = fields.Integer("C_PPH21")
    C_BPJSKES_COM   = fields.Integer("C_PPH21")
    C_PENCOM        = fields.Integer("C_PPH21")
    NET             = fields.Integer("NET")

