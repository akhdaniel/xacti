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
                "I_THR",
                "I_BONUS",
                "I_TPK",
                "I_OCCUP",
                "I_FAMILY",
                "I_FUNCTIONAL",
                "I_MEDIC",
                "I_TRANSPORT",
                "I_PERFORM",
                "D_PPH21",
                "D_TRANSPORT",
                "NET"
            ) 
            SELECT 
                %s,
                emp.x_idno, 

                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='BASIC'),0) + 
                coalesce((select amount from hr_payslip_line where slip_id=ps.id and code='I_BASIC'), 0) - 
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='D_BASIC'),0) as BASIC,

                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='I_THR'),0) as I_THR,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='I_BONUS'),0) as I_BONUS,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='I_TPK'),0) as I_TPK,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='I_OCCUP'),0) as I_OCCUP,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='I_FAMILY'),0) as I_FAMILY,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='I_FUNCTIONAL'),0) as I_FUNCTIONAL,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='I_MEDIC'),0) as I_MEDIC,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='I_PERFORM'),0) as I_PERFORM,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='I_TRANSPORT'),0) as I_TRANSPORT,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='D_PPH21'),0) as D_PPH21,
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='D_TRANSPORT'),0) as D_TRANSPORT,
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
        worksheet.write("C1", "I_THR", bold)
        worksheet.write("D1", "I_BONUS", bold)
        worksheet.write("E1", "I_TPK", bold)
        worksheet.write("F1", "I_OCCUP", bold)
        worksheet.write("H1", "I_FAMILY", bold)
        worksheet.write("G1", "I_FUNCTIONAL", bold)
        worksheet.write("I1", "I_MEDIC", bold)
        worksheet.write("I1", "I_PERFORM", bold)
        worksheet.write("J1", "I_TRANSPORT", bold)
        worksheet.write("K1", "D_PPH21", bold)
        worksheet.write("L1", "D_TRANSPORT", bold)
        worksheet.write("M1", "NET", bold)

        # write data 
        row = 1
        for line in self.detail_ids:
            worksheet.write(row, 0, line.IDNO)
            worksheet.write(row, 1, line.BASIC, numeric)
            worksheet.write(row, 2, line.I_THR, numeric)
            worksheet.write(row, 3, line.I_BONUS, numeric)
            worksheet.write(row, 4, line.I_TPK, numeric)
            worksheet.write(row, 5, line.I_OCCUP, numeric)
            worksheet.write(row, 7, line.I_FAMILY, numeric)
            worksheet.write(row, 6, line.I_FUNCTIONAL, numeric)
            worksheet.write(row, 8, line.I_MEDIC, numeric)
            worksheet.write(row, 8, line.I_PERFORM, numeric)
            worksheet.write(row, 9, line.I_TRANSPORT, numeric)
            worksheet.write(row, 10, line.D_PPH21, numeric)
            worksheet.write(row, 11, line.D_TRANSPORT, numeric)
            worksheet.write(row, 12, line.NET, numeric)
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
    I_THR           = fields.Integer("I_THR")
    I_BONUS         = fields.Integer("I_BONUS")
    I_TPK           = fields.Integer("I_TPK")
    I_OCCUP         = fields.Integer("I_OCCUP")
    I_FAMILY        = fields.Integer("I_FAMILY")
    I_FUNCTIONAL    = fields.Integer("I_FUNCTIONAL")
    I_PERFORM       = fields.Integer("I_MEDIC")
    I_TRANSPORT     = fields.Integer("I_TRANSPORT")
    D_PPH21         = fields.Integer("D_PPH21")
    D_TRANSPORT     = fields.Integer("D_TRANSPORT")
    NET             = fields.Integer("NET")

