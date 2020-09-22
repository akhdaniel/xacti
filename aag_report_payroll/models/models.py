# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)



class report_header(models.Model):
    _name = 'aag.report_header'
    _description = 'payroll header'

    name = fields.Char("Name")
    month = fields.Integer("Month")
    year = fields.Integer("Year")

    detail_ids = fields.One2many(comodel_name="aag.report_detail", inverse_name="header_id")



    def action_generate(self):
        _logger.info("--- action_generate")


    def action_export(self):
        _logger.info("--- action_export")


class report_detail(models.Model):
    _name = 'aag.report_detail'
    _description = 'payroll detail'

    header_id = fields.Many2one(comodel_name="aag.report_header")

    idno = fields.Integer("IDNO")
    wage = fields.Integer("Wage")
    transport = fields.Integer("Transport")

