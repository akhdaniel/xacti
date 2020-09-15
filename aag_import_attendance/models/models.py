# -*- coding: utf-8 -*-
from odoo import models, fields, api
import pypyodbc
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)



ip_address="172.17.145.17"
user="user_postgresql"
password="Postgresql"
port="1433"
database="HRD"

class employee(models.Model):
    _name = "hr.employee"
    _inherit = "hr.employee"

    def process_import(self):

        #---- connection and create cursor
        cs = 'DRIVER={ODBC Driver 17 for SQL Server};PORT='+port+';SERVER='+ip_address+';DATABASE='+database+';UID='+user+';PWD='+password
        cnn = pypyodbc.connect(cs, unicode_results=True)
        cur = cnn.cursor()

        #---- query database
        sql = "select IDNO,CHECKTIME_IN,CHECKTIME_OUT from ANVIZ_ABS_FOR_ODOO where CHECKTIME_IN IS NOT NULL"
        cur.execute(sql)
        records = cur.fetchall()

        #---- process results
        sql = """insert into hr_attendance (employee_id, check_in, check_out) VALUES """

        for rec in records:
            IDNO = int(rec[0])
            CHECKTIME_IN=rec[1]
            CHECKTIME_OUT=rec[2]
            employee_id = self.get_employee_id(IDNO)
            sql += str((employee_id, CHECKTIME_IN.strftime("%Y-%m-%d %H:%I:%S"), CHECKTIME_OUT.strftime("%Y-%m-%d %H:%I:%S")))

        _logger.info("sql ==== %s", sql)

    def get_employee_id(self, IDNO):
        sql = "select id from hr_employee where x_idno=%s" % IDNO
        cr = self.env.cr 
        cr.execute(sql)
        result = cr.fetchone()
        if not result:
            raise UserError('IDNO tidak ditemukan')
        
        return result[0]
