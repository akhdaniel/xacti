# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)
import xlsxwriter

import base64
from io import BytesIO
# from io import StringIO

class report_spmi_header(models.Model):
    _name = 'aag.report_spmi_header'
    _description = 'report spmi header'

    name = fields.Char("Name")
    month = fields.Integer("Month")
    year = fields.Integer("Year")

    export_file = fields.Binary("Export File")
    export_filename = fields.Char(string="Export File Name",  )

    detail_ids = fields.One2many(comodel_name="aag.report_spmi_detail", inverse_name="header_id")

    def action_generate(self):
        cr = self.env.cr

        sql = "delete from aag_report_spmi_detail where header_id=%s"
        cr.execute(sql, (self.id,))

        sql = """
            INSERT INTO aag_report_spmi_detail (
                header_id,
                "IDNO",
                "NAME",
                "ALLCD",
                "EMPSTS",
                "DEPT",
                "SECT",
                "SBSEC",
                "DESC",
                "SPMICOS",
                "SPMIMED",
                "TTL_SPMI",
                "SEX"
            ) 
            SELECT 
                %s,
                emp.x_idno, emp.name,
                case 
                    when emp.x_allcd isnull then '  '
                    else emp.x_allcd
                end as ALLCD,
                emp.x_empsts as EMPSTS, emp.x_dept as DEPT, emp.x_sect as SECT, emp.x_sbsec as SBSEC, dept.x_desc as DESC,
                ps.d_spmicos as SPMICOS,
                ps.d_spmimed as SPMIMED,
                ps.d_spmi as TTL_SPMI,
                case 
                    when emp.gender='male' then 'M'
                    else 'F'
                end as SEX
            from 
                hr_payslip ps 
            join 
                hr_employee emp on ps.employee_id = emp.id
            join 
                aag_dept_master_aag_dept_master dept on dept.x_dept = emp.x_dept
                and dept.x_sect = emp.x_sect
                and dept.x_sbsec = emp.x_sbsec

            where
                date_part('month', ps.date_to) = %s
                and date_part('year', ps.date_to) = %s
                and emp.x_spmi = 'True'

        """
        cr.execute(sql, (self.id, self.month, self.year))

        # _logger.info("--- done action_generate")
        # simpan 

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
        worksheet.set_column('B:B', 10)  # Column  B width set to 10.
        worksheet.set_column('C:C', 30)  # Columns C width set to 30.
        worksheet.set_column('D:D', 10)  
        worksheet.set_column('E:E', 10)  
        worksheet.set_column('F:F', 10)  
        worksheet.set_column('G:G', 10)  
        worksheet.set_column('H:H', 35)  
        worksheet.set_column('I:I', 10)  

        # write header
        worksheet.write("B2", "PT. XACTI INDONESIA", font14)
        worksheet.write("B3", "DAFTAR PEMOTONGAN COS DAN SUMBANGAN MEDICAL SPMI", font12)
        worksheet.write("B5", "IDNO", bold)
        worksheet.write("C5", "NAMA", bold)
        worksheet.write("D5", "KODE GOL.", bold)
        worksheet.write("E5", "SPMI-COS", bold)
        worksheet.write("F5", "SPMI-MED", bold)
        worksheet.write("G5", "TTL_SPMI", bold)
        worksheet.write("H5", "DEPT/SECTION", bold)
        worksheet.write("I5", "JNS. KEL.", bold)

        # write data 
        row = 5
        for line in self.detail_ids:
            worksheet.write(row, 1, line.IDNO)
            worksheet.write(row, 2, line.NAME)
            worksheet.write(row, 3, line.ALLCD)
            worksheet.write(row, 4, line.SPMICOS, numeric)
            worksheet.write(row, 5, line.SPMIMED, numeric)
            worksheet.write(row, 6, line.TTL_SPMI, numeric)
            worksheet.write(row, 7, line.DESC)
            worksheet.write(row, 8, line.SEX)

            row += 1

        workbook.close()

        file_data.seek(0)
        self.export_file = base64.encodestring(file_data.getvalue())
        self.export_filename = 'Report_SPMI-%s-%s.xlsx' % (self.month, self.year)

        #_logger.info("--- action_export")


class report_spmi_detail(models.Model):
    _name = 'aag.report_spmi_detail'
    _description = 'payroll spmi detail'

    header_id = fields.Many2one(comodel_name="aag.report_spmi_header")

    IDNO            = fields.Integer("IDNO")
    NAME            = fields.Char("NAME")
    ALLCD           = fields.Char("ALLW. CODE")
    EMPSTS          = fields.Char("EMPSTS")
    DIRECT          = fields.Char("DIRECT")
    DEPT            = fields.Integer("DEPT")
    SECT            = fields.Integer("SECT")
    SBSEC           = fields.Integer("SBSEC")
    DESC            = fields.Char("DEPT/SECTION")
    SPMICOS         = fields.Integer("SPMI COS")
    SPMIMED         = fields.Integer("SPMI MED")
    TTL_SPMI        = fields.Integer("TOTAL SPMI")
    SEX             = fields.Char("JNS KEL.")
