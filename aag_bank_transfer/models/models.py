# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

import base64
from io import BytesIO
# from io import StringIO

class export_text_header(models.Model):
    _name = 'aag.export_text_header'
    _description = 'text file header'

    name = fields.Char("Name")
    year = fields.Integer("Year")
    month = fields.Integer("Month")
    day = fields.Integer("Day")

    export_file = fields.Binary("Export File")
    export_filename = fields.Char(string="Export File Name",  )

    detail_ids = fields.One2many(comodel_name="aag.export_text_detail", inverse_name="header_id")

    def action_generate(self):
        cr = self.env.cr

        sql = "delete from aag_export_text_detail where header_id=%s"
        cr.execute(sql, (self.id,))

        sql = """
            INSERT INTO aag_export_text_detail (
                header_id,
                "IDNO",
                "ACCNAME",
                "BRANCH",
                "PAYCODE",
                "ACCNO",
                "CURR1",
                "AMOUNT",
                "CURR2",
                "REMARK"
            ) 
            SELECT 
                %s,
                emp.x_idno,
                emp.x_accname,
                'DEPOK',
                'P',
                emp.x_accno,
                'IDR',
                coalesce((select coalesce(amount,0) from hr_payslip_line where slip_id=ps.id and code='NET'),0) as NET,
                'IDR',
                'GAJI'
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
        
        # write header
        file_data.write('XACTIINDONESIA'.ljust(30).encode())
        file_data.write('XACTIINDO'.ljust(12).encode())
        file_data.write('BLIDR10001'.encode())
        year=self.year
        month=self.month
        day=self.day
        file_data.write(('%04d%02d%02d' %(year,month,day)).encode())
        file_data.write('IDR'.ljust(10).encode())
        file_data.write('584800000799'.encode())
        file_data.write('\n'.encode())
        
        # write data 
        row = 1
        for line in self.detail_ids:
            if not line.ACCNAME:
                raise UserError('Acc. Name Not Found IDNO=%s' %line.IDNO)
            file_data.write((line.IDNO).rjust(7,'0').ljust(20).encode())
            file_data.write((line.ACCNAME).ljust(40).encode())
            file_data.write((line.BRANCH).ljust(105).encode())
            file_data.write((line.PAYCODE).encode())
            file_data.write((line.ACCNO).ljust(34).encode())
            file_data.write((line.CURR1).encode())
            file_data.write('{:.2f}'.format(line.AMOUNT).rjust(18,'0').encode())
            file_data.write((line.CURR2).encode())
            file_data.write((line.REMARK).ljust(444).encode())
        # Write CR (Pindah Baris(Enter))
            file_data.write(' \n'.encode())

            row += 1


        file_data.seek(0)
        self.export_file = base64.encodestring(file_data.getvalue())
        self.export_filename = 'Export_text-%s-%s.txt' % (self.month, self.year)

        _logger.info("--- action_export")


class export_text_detail(models.Model):
    _name = 'aag.export_text_detail'
    _description = 'export text detail'

    header_id = fields.Many2one(comodel_name="aag.export_text_header")

    IDNO            = fields.Char("IDNO")
    ACCNAME         = fields.Char("BANK ACC NAME")
    BRANCH          = fields.Char("BRANCH")
    PAYCODE         = fields.Char("PAYMENT CODE")
    ACCNO           = fields.Char("BANK ACC#")
    CURR1           = fields.Char("CURRENCY-1")
    AMOUNT          = fields.Float("AMOUNT")
    CURR2           = fields.Char("CURRENCY-2")
    REMARK          = fields.Char("REMARK")

