# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)
import xlsxwriter

import base64
from io import BytesIO
# from io import StringIO

class report_summary_header(models.Model):
    _name = 'aag.report_summary_header'
    _description = 'payroll header'

    name = fields.Char("Name")
    month = fields.Integer("Month")
    year = fields.Integer("Year")

    export_file = fields.Binary("Export File")
    export_filename = fields.Char(string="Export File Name",  )

    detail_ids = fields.One2many(comodel_name="aag.report_summary_detail", inverse_name="header_id")

    def action_generate(self):
        cr = self.env.cr

        sql = "delete from aag_report_summary_detail where header_id=%s"
        cr.execute(sql, (self.id,))

        sql = """
            INSERT INTO aag_report_summary_detail (
                header_id,
                "DEPT",
                "BASIC",
                "NET"
            ) 
            select 
            %s,
            dept.id,
            (select sum(amount) from hr_payslip_line line 
                join hr_payslip ps on line.slip_id=ps.id  
                join hr_employee emp on ps.employee_id = emp.id
                where code='BASIC' and emp.department_id = dept.id and date_part('month', ps.date_to) = %s and date_part('year', ps.date_to) = %s) as BASIC,
            (select sum(amount) from hr_payslip_line line 
                join hr_payslip ps on line.slip_id=ps.id  
                join hr_employee emp on ps.employee_id = emp.id
                where code='NET' and emp.department_id = dept.id and date_part('month', ps.date_to) = %s and date_part('year', ps.date_to) = %s) as NET
            from hr_department dept
        """
        cr.execute(sql, (self.id, self.month, self.year, self.month, self.year))

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
        worksheet.write("C1", "I_TRANSPORT", bold)
        worksheet.write("D1", "D_PPH21", bold)
        worksheet.write("E1", "D_TRANSPORT", bold)
        worksheet.write("F1", "NET", bold)

        # write data 
        row = 1
        for line in self.detail_ids:
            worksheet.write(row, 0, line.IDNO)
            worksheet.write(row, 1, line.BASIC, numeric)
            worksheet.write(row, 2, line.I_TRANSPORT, numeric)
            worksheet.write(row, 3, line.D_PPH21, numeric)
            worksheet.write(row, 4, line.D_TRANSPORT, numeric)
            worksheet.write(row, 5, line.NET, numeric)
            row += 1

        workbook.close()

        file_data.seek(0)
        self.export_file = base64.encodestring(file_data.getvalue())
        self.export_filename = 'report_payroll-%s-%s.xlsx' % (self.month, self.year)




        _logger.info("--- action_export")


class report_summary_detail(models.Model):
    _name = 'aag.report_summary_detail'
    _description = 'payroll detail'

    header_id = fields.Many2one(comodel_name="aag.report_summary_header")

    DEPT            = fields.Integer("DEPT")
    BASIC           = fields.Integer("BASIC")
    I_TRANSPORT     = fields.Integer("I_TRANSPORT")
    D_PPH21         = fields.Integer("D_PPH21")
    D_TRANSPORT     = fields.Integer("D_TRANSPORT")
    NET             = fields.Integer("NET")

